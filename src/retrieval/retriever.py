from openai import OpenAI
from src.config import CHROMA_PATH, EMBEDDING_MODEL, TOP_K, OPENAI_API_KEY
import chromadb
import re


def retrieve(query: str) -> list:
    """Embed the query and retrieve the most relevant chunks from Chroma."""
    client = OpenAI(api_key=OPENAI_API_KEY)
    db = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = db.get_or_create_collection(name="eu_ai_act")

    match = re.search(r'Article \d+', query)
    if match:
        article = match.group()
        results = collection.get(where={"article": article})
        return [{"text": doc, "article": meta["article"]}
                for doc, meta in zip(results["documents"], results["metadatas"])]
    else:
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