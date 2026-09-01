# EU AI Act RAG

A retrieval-augmented generation (RAG) system for querying the EU AI Act
in natural language. Ask questions about AI regulation and get answers
grounded in the actual legislative text, with source references to
specific articles.

Implemented for greater understanding of the full RAG pipeline.

## How it works

The system operates in two distinct phases:

**Phase 1 — Indexing (runs once)**
The EU AI Act is loaded, split into chunks on article boundaries,
embedded into vectors using a local sentence-transformers model, and
stored in a Chroma vector database.

**Phase 2 — Query (runs per question)**
The question is embedded using the same model, a similarity search
finds the most relevant article chunks, and Claude generates a grounded
answer with explicit article references.

```
Document → Chunking → Embeddings → Chroma
Question → Embeddings → Similarity search → Claude → Answer + sources
```

## Key design decisions

**Article-boundary chunking** — chunks follow the EU AI Act's own
semantic structure rather than fixed token counts, preserving the
meaning of each legislative unit

**Same embedding model for indexing and queries** — chunks and questions
must share the same vector space for similarity search to be meaningful

**Hybrid retrieval** — direct article lookup via metadata filter for
queries referencing specific articles (e.g. "summarise Article 12"),
semantic similarity search for open-ended questions

**No LangChain** — each component (loader, chunker, embedder, retriever,
generator) is implemented explicitly, making the data flow transparent
and each step independently testable

**Source attribution** — every answer includes the specific articles it
draws from, enabling verification against the source document

## Tech Stack

| Component       | Technology                               |
| --------------- | ---------------------------------------- |
| Embeddings      | sentence-transformers / all-MiniLM-L6-v2 |
| Vector database | Chroma                                   |
| LLM             | Claude (Anthropic API)                   |
| API layer       | FastAPI                                  |
| Language        | Python 3.12                              |

## Project structure

```
eu-ai-act-rag/
├── src/
│   ├── ingestion/       # Phase 1: load, chunk, embed
│   ├── retrieval/       # Phase 2: similarity search
│   ├── generation/      # Phase 2: prompt building and Claude call
│   ├── api/             # FastAPI app and router
│   └── config.py
├── data/                # EU AI Act source document (not committed)
├── main.py              # CLI entry point
└── requirements.txt
```

## Getting Started

### Prerequisites

Python 3.12+, Anthropic API key

### Setup

```bash
git clone https://github.com/vita-tak/eu-ai-act-rag.git
cd eu-ai-act-rag

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
# Add your ANTHROPIC_API_KEY and ANTHROPIC_WORKSPACE_ID to .env
```

Add the EU AI Act as a text file at `data/eu_ai_act.txt`. The official
text is available [here](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689).

### Run CLI

```bash
python main.py
```

The first run indexes the document automatically. Subsequent runs go
straight to the query interface.

### Run API

```bash
uvicorn src.api.app:app --reload
```

API documentation available at `http://localhost:8000/docs`.

#### POST /query

```json
{
  "question": "What are the obligations for high-risk AI systems?"
}
```

Response:

```json
{
  "answer": "...",
  "sources": ["Article 16", "Article 9", "Article 14"]
}
```

## Why this project

This project implements each step of the RAG pipeline explicitly: chunking
strategy, embedding model selection, vector storage, retrieval, and prompt
construction.

The EU AI Act is the domain because it is the regulatory framework that
governs AI systems in Europe. Understanding it programmatically is directly
relevant to building compliant AI applications.
