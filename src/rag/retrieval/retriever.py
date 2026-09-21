from openai import OpenAI
from flashrank import Ranker, RerankRequest
from src.config import CHROMA_PATH, EMBEDDING_MODEL, TOP_K, OPENAI_API_KEY, RERANK_CANDIDATES
import chromadb
import re

# Load the re-ranker once at module level to avoid reloading on every call.
ranker = Ranker()


def retrieve(query: str) -> list:
    """
    Hybrid retrieval from the EU AI Act vector store.

    Uses keyword-based metadata filtering when the query references a specific
    article (e.g. "Article 12"), and falls back to semantic similarity search
    using embeddings for open-ended questions. Similarity search results are
    re-ranked before being returned.

    Args:
        query: The user's natural language question.

    Returns:
        A list of dicts with "text" and "article" keys.
    """
    client = OpenAI(api_key=OPENAI_API_KEY)
    db = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = db.get_or_create_collection(name="eu_ai_act")

    # Check if the query references a specific article number.
    # If so, use direct metadata filtering for exact lookup.
    # Re-ranking is skipped here since the results are already exact matches.
    match = re.search(r'Article \d+', query)
    if match:
        article = match.group()
        results = collection.get(where={"article": article})
        return [{"text": doc, "article": meta["article"]}
                for doc, meta in zip(results["documents"], results["metadatas"])]

    # No article reference found: embed the query and run semantic search.
    # Fetch RERANK_CANDIDATES chunks so the re-ranker has room to work.
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=[query]
    )
    query_embedding = response.data[0].embedding

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=RERANK_CANDIDATES
    )
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    # Re-rank the candidates by relevance to the query.
    # RerankRequest takes the query and a list of passage dicts.
    passages = [{"id": i, "text": doc} for i, doc in enumerate(documents)]
    rerank_request = RerankRequest(query=query, passages=passages)
    reranked = ranker.rerank(rerank_request)

    # Keep only the top TOP_K results after re-ranking,
    # and map back to the original metadata using the passage id.
    top = reranked[:TOP_K]
    return [{"text": passages[r["id"]]["text"], "article": metadatas[r["id"]]["article"]}
            for r in top]