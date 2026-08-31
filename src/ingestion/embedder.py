from sentence_transformers import SentenceTransformer
import chromadb
from src.config import CHROMA_PATH, EMBEDDING_MODEL


def embed_and_store(chunks: list) -> None:
    """Embed all chunks and store them in Chroma with metadata."""
    model = SentenceTransformer(EMBEDDING_MODEL)
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection(name="eu_ai_act")

    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(texts)

    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        collection.add(
            documents=[chunk["text"]],
            embeddings=[embedding.tolist()],
            metadatas=[{"article": chunk["article"]}],
            ids=[str(i)]
        )