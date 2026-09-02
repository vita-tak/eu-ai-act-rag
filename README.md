# EU AI Act RAG + Compliance Agent

A retrieval-augmented generation (RAG) system for querying the EU AI Act
in natural language, extended with an agentic compliance classifier that
determines the risk category of an AI product under the EU AI Act.

Implemented for greater understanding of the full RAG pipeline and
agentic tool use patterns.

## System overview

The project consists of two layers:

**Layer 1 - RAG system**
Ask questions about the EU AI Act in natural language and get answers
grounded in the actual legislative text, with source references to
specific articles.

**Layer 2 - Compliance agent**
Submit a product description and the agent classifies it under the EU
AI Act risk framework. The agent searches the RAG system, asks
follow-up questions when information is missing, and produces a
structured report with classification, reasoning, and cited articles.

The agent is multi-turn: it pauses when it needs clarification, returns
a question to the caller, and resumes when the answer arrives. Sessions
are maintained server-side by session ID.

## How it works

### RAG pipeline

**Phase 1 - Indexing (runs once)**
The EU AI Act is loaded, split into chunks on article boundaries,
embedded into vectors using OpenAI embeddings, and stored in a Chroma
vector database.

**Phase 2 - Query (runs per question)**
The question is embedded using the same model, a similarity search
finds the most relevant article chunks, and Claude generates a grounded
answer with explicit article references.

```
Document -> Chunking -> Embeddings -> Chroma
Question -> Embeddings -> Similarity search -> Claude -> Answer + sources
```

### Compliance agent (ReAct loop)

The agent runs a tool use loop until it has enough information to
classify the product:

```
Product description -> Agent loop:
  search_eu_ai_act  -> POST /query (RAG system)
  ask_user          -> follow-up question returned to caller
  generate_report   -> structured classification report
```

The loop runs until the agent calls generate_report or hits the
max_steps safety limit.

## Key design decisions

**Article-boundary chunking** - chunks follow the EU AI Act's own
semantic structure rather than fixed token counts, preserving the
meaning of each legislative unit

**Same embedding model for indexing and queries** - chunks and questions
must share the same vector space for similarity search to be meaningful

**Hybrid retrieval** - direct article lookup via metadata filter for
queries referencing specific articles (e.g. "summarise Article 12"),
semantic similarity search for open-ended questions

**Source attribution** - every answer includes the specific articles it
draws from, enabling verification against the source document

**Agent as API consumer** - the compliance agent calls the RAG system
via HTTP rather than importing it directly, keeping the two layers
independently deployable

**Session-based multi-turn** - agent state (the messages list) is stored
server-side by session ID, allowing the caller to answer follow-up
questions across multiple HTTP requests

**FollowUpRequired exception** - when running in API mode, ask_user
raises an exception instead of blocking on input(), which signals the
loop to pause and return the question to the caller

## Risk classifications

The agent classifies products into one of six categories:

- Not an AI system
- Minimal risk
- Limited risk
- High risk
- GPAI
- Prohibited practice

## Tech stack

| Component       | Technology                    |
| --------------- | ----------------------------- |
| Embeddings      | OpenAI text-embedding-3-small |
| Vector database | Chroma                        |
| LLM             | Claude Haiku (Anthropic API)  |
| API layer       | FastAPI                       |
| Language        | Python 3.12                   |

## Project structure

```
eu-ai-act-rag/
├── src/
│   ├── ingestion/       # Phase 1: load, chunk, embed
│   ├── retrieval/       # Phase 2: similarity search
│   ├── generation/      # Phase 2: prompt building and Claude call
│   ├── agent/
│   │   ├── agent.py     # ReAct loop and session logic
│   │   └── tools.py     # Tool definitions and implementations
│   ├── api/             # FastAPI app and router
│   └── config.py
├── data/                # EU AI Act source document (not committed)
├── main.py              # CLI entry point for RAG system
└── requirements.txt
```

## Getting started

### Prerequisites

Python 3.12+, Anthropic API key, OpenAI API key

### Setup

```bash
git clone https://github.com/vita-tak/eu-ai-act-rag.git
cd eu-ai-act-rag

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
# Add your ANTHROPIC_API_KEY, ANTHROPIC_WORKSPACE_ID and OPENAI_API_KEY to .env
```

Add the EU AI Act as a text file at `data/eu_ai_act.txt`. The official
text is available [here](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689).

### Run CLI (RAG only)

```bash
python main.py
```

The first run indexes the document automatically. Subsequent runs go
straight to the query interface.

### Run API

```bash
PYTHONPATH=. uvicorn src.api.app:app --reload
```

API documentation available at `http://localhost:8000/docs`.

## API reference

### POST /query

Ask a question about the EU AI Act.

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

### POST /classify/start

Start a compliance classification session.

```json
{
  "product_description": "An AI that screens job applications and ranks candidates."
}
```

Response when follow-up is needed:

```json
{
  "status": "follow_up",
  "session_id": "...",
  "question": "Does this system make autonomous hiring decisions?"
}
```

Response when classification is complete:

```json
{
  "status": "done",
  "session_id": "...",
  "classification": "High risk",
  "reasoning": "...",
  "cited_articles": ["Annex III, Section 4(a)", "Article 9", "Article 14"]
}
```

### POST /classify/answer

Continue a classification session with an answer to a follow-up question.

```json
{
  "session_id": "...",
  "answer": "No, humans make the final hiring decision."
}
```

Response follows the same format as /classify/start.

## Why this project

This project implements each step of the RAG pipeline explicitly:
chunking strategy, embedding model selection, vector storage, retrieval,
and prompt construction.

The compliance agent extends this with agentic tool use: a ReAct loop
where Claude decides which tools to call, your code executes them, and
the results feed back into the next decision. The multi-turn session
pattern is directly applicable to any agent that needs to gather
information before producing a result.

The EU AI Act is the domain because it is the regulatory framework that
governs AI systems in Europe. Understanding it programmatically is
directly relevant to building compliant AI applications.
