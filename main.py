import os
from src.ingestion.loader import load_document
from src.ingestion.chunker import chunk_document
from src.ingestion.embedder import embed_and_store
from src.retrieval.retriever import retrieve
from src.generation.generator import generate
from src.config import CHROMA_PATH


def index():
    """Run the indexing pipeline (Phase 1)."""
    print("Loading document...")
    text = load_document()

    print("Chunking document...")
    chunks = chunk_document(text)
    print(f"Created {len(chunks)} chunks.")

    print("Embedding and storing in Chroma...")
    embed_and_store(chunks)
    print("Indexing complete.")


def query(question: str):
    """Run the query pipeline (Phase 2)."""
    print("Retrieving relevant chunks...")
    chunks = retrieve(question)

    print("Generating answer...")
    result = generate(question, chunks)

    print("\n--- Answer ---")
    print(result["answer"])
    print("\n--- Sources ---")
    print(", ".join(result["sources"]))


if __name__ == "__main__":
    if not os.path.exists(CHROMA_PATH):
        print("No index found. Running indexing pipeline first...")
        index()

    print("\nEU AI Act RAG System")
    print("Type 'quit' to exit.\n")

    while True:
        question = input("Your question: ")
        if question.lower() == "quit":
            break
        query(question)
        print()