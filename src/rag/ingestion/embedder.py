from openai import OpenAI
import chromadb
from src.config import CHROMA_PATH, EMBEDDING_MODEL, OPENAI_API_KEY


def embed_and_store(chunks: list) -> None:
    """Embed all chunks and store them in Chroma with metadata."""
    client = OpenAI(api_key=OPENAI_API_KEY)
    db = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = db.get_or_create_collection(name="eu_ai_act")

    texts = [chunk["text"] for chunk in chunks]

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts
    )

    embeddings = [item.embedding for item in response.data]

    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        collection.add(
            documents=[chunk["text"]],
            embeddings=[embedding],
            metadatas=[{"article": chunk["article"]}],
            ids=[str(i)]
        )