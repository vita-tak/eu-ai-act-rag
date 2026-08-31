from sentence_transformers import SentenceTransformer
from src.config import CHROMA_PATH, EMBEDDING_MODEL, TOP_K
import chromadb

def retrieve(query: str) -> list:
    """Embed the query and retrieve the most relevant chunks from Chroma."""
    model = SentenceTransformer(EMBEDDING_MODEL)
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection(name="eu_ai_act")

    results = collection.query(
        query_embeddings=model.encode([query]).tolist(),
        n_results=TOP_K
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    return [{"text": doc, "article": meta["article"]} for doc, meta in zip(documents, metadatas)]