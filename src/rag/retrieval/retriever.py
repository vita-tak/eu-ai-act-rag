from openai import OpenAI
from src.config import CHROMA_PATH, EMBEDDING_MODEL, TOP_K, OPENAI_API_KEY
import chromadb
import re


def retrieve(query: str) -> list:
    """
    Hybrid retrieval from the EU AI Act vector store.

    Uses keyword-based metadata filtering when the query references a specific
    article (e.g. "Article 12"), and falls back to semantic similarity search
    using embeddings for open-ended questions.

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
    match = re.search(r'Article \d+', query)
    if match:
        article = match.group()
        results = collection.get(where={"article": article})
        return [{"text": doc, "article": meta["article"]}
                for doc, meta in zip(results["documents"], results["metadatas"])]

    # No article reference found: embed the query and run semantic search
    # to find the most relevant chunks by vector similarity.
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=[query]
    )
    query_embedding = response.data[0].embedding

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=TOP_K
    )
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    return [{"text": doc, "article": meta["article"]}
            for doc, meta in zip(documents, metadatas)]