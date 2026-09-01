from sentence_transformers import SentenceTransformer
from src.config import CHROMA_PATH, EMBEDDING_MODEL, TOP_K
import chromadb
import re

def retrieve(query: str) -> list:
    """Embed the query and retrieve the most relevant chunks from Chroma."""
    model = SentenceTransformer(EMBEDDING_MODEL)
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection(name="eu_ai_act")

    match = re.search(r'Article \d+', query)
    if match:
        article = match.group()
        results = collection.get(where={"article": article})
        return [{"text": doc, "article": meta["article"]} 
                for doc, meta in zip(results["documents"], results["metadatas"])]
    else:
        results = collection.query(
            query_embeddings=model.encode([query]).tolist(),
            n_results=TOP_K
        )
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        return [{"text": doc, "article": meta["article"]} 
                for doc, meta in zip(documents, metadatas)]