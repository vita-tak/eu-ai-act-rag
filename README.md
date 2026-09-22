# EU AI Act RAG + Compliance Agent

A retrieval-augmented generation (RAG) system for querying the EU AI Act
in natural language, extended with an agentic compliance classifier that
determines the risk category of an AI product under the EU AI Act.

Implemented for greater understanding of the full RAG pipeline and
agentic tool use patterns.

## System overview

The project consists of three layers:

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

**Layer 3 - Chat interface**
A unified chat endpoint that lets users mix EU AI Act questions and
compliance classifications freely in the same conversation. An intent
classifier routes each message to the correct flow, and a state machine
tracks ongoing classifications so the agent can be resumed when the
user answers a follow-up question.

## How it works

### RAG pipeline

**Phase 1 - Indexing (runs once, locally)**
The EU AI Act PDF is parsed by Docling, which preserves the document's
semantic structure and exports it as Markdown. The Markdown is split
into chunks on heading boundaries, embedded into vectors using OpenAI
embeddings, and stored in a Chroma vector database. The finished
database is committed and deployed as a static file — Docling is a
local build-time tool and is never installed in production.

**Phase 2 - Query (runs per question)**
The question is embedded using the same model, a similarity search
finds the most relevant article chunks, a re-ranker sorts them by
relevance, and Claude generates a grounded answer with explicit article
references.

```
PDF -> Docling -> Markdown -> Chunking -> Embeddings -> Chroma
Question -> Embeddings -> Similarity search -> Re-ranking -> Claude -> Answer + sources
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

### Chat interface (intent classification)

Each message is classified into one of three intents before being routed:

```
POST /chat
  message -> intent classifier -> rag_query        -> RAG pipeline
                               -> risk_classification -> agent loop
                               -> risk_classification_followup -> resume agent
```

If a classification is in progress and the user switches topic, the
ongoing session is abandoned and the new intent is handled instead.

## Key design decisions

**Docling for PDF parsing** - Docling understands PDF layout and
preserves the document's hierarchical structure (headings, sections,
lists) when exporting to Markdown. This produces more reliable chunks
than raw text extraction.

**Markdown-boundary chunking** - chunks follow the document's own
heading structure rather than fixed token counts or regex patterns,
preserving the semantic meaning of each legislative unit.

**Same embedding model for indexing and queries** - chunks and questions
must share the same vector space for similarity search to be meaningful.

**Re-ranking** - similarity search returns RERANK_CANDIDATES candidates,
which are re-ranked by a local flashrank model before the top TOP_K
results are sent to Claude. This improves relevance over pure vector
similarity.

**Hybrid retrieval** - direct article lookup via metadata filter for
queries referencing specific articles (e.g. "summarise Article 12"),
semantic similarity search with re-ranking for open-ended questions.

**Source attribution** - every answer includes the specific articles it
draws from, enabling verification against the source document.

**Agent as API consumer** - the compliance agent calls the RAG system
via HTTP rather than importing it directly, keeping the two layers
independently deployable.

**Session-based multi-turn** - agent state (the messages list) is stored
server-side by session ID, allowing the caller to answer follow-up
questions across multiple HTTP requests.

**FollowUpRequired exception** - when running in API mode, ask_user
raises an exception instead of blocking on input(), which signals the
loop to pause and return the question to the caller.

**tool_use_id injection** - when the agent pauses for a follow-up, the
tool_use_id is returned to the caller. The user's answer is injected as
a proper tool_result block with the matching id when the conversation
resumes, preserving the correct message format for the Anthropic API.

**Intent classification** - a small LLM classifier (Claude Haiku,
max_tokens=100) routes each message to the correct flow based on message
content and current conversation state.

**Indexing is a local build step** - Docling is a development-only
dependency and is never installed in production. The Chroma database is
built locally and deployed as a static file.

## Risk classifications

The agent classifies products into one of six categories:

- Not an AI system
- Minimal risk
- Limited risk
- High risk
- GPAI
- Prohibited practice

## Tech stack

| Component         | Technology                    |
| ----------------- | ----------------------------- |
| PDF parsing       | Docling (local, build-time)   |
| Embeddings        | OpenAI text-embedding-3-small |
| Vector database   | Chroma                        |
| Re-ranking        | flashrank                     |
| LLM               | Claude Haiku (Anthropic API)  |
| Intent classifier | Claude Haiku (Anthropic API)  |
| API layer         | FastAPI                       |
| Language          | Python 3.12                   |

## Project structure

```
eu-ai-act-rag/
├── src/
│   ├── rag/
│   │   ├── ingestion/   # loader (Docling), chunker, embedder
│   │   ├── retrieval/   # hybrid search + re-ranking
│   │   └── generation/  # prompt building and Claude call
│   ├── agent/
│   │   ├── agent.py     # ReAct loop and session logic
│   │   └── tools.py     # tool definitions and implementations
│   ├── chat/
│   │   ├── intent.py    # intent classifier
│   │   ├── conversation.py  # state machine per conversation_id
│   │   └── router.py    # routes messages to correct flow
│   ├── api/             # FastAPI app and router
│   └── config.py
├── tests/
│   └── evals/           # DeepEval agent evals
├── data/                # EU AI Act PDF (not committed)
├── chroma_db/           # pre-built vector database (committed)
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

The Chroma database is included in the repository and ready to use.
To rebuild it from a new PDF, install Docling locally (not in requirements.txt):

```bash
pip install docling
```

Add the EU AI Act PDF at `data/eu_ai_act.pdf` and run:

```bash
python main.py
```

The first run detects a missing database and rebuilds it automatically.

### Run CLI (RAG only)

```bash
python main.py
```

### Run API

```bash
PYTHONPATH=. uvicorn src.api.app:app --reload
```

API documentation available at `http://localhost:8000/docs`.

## API reference

### POST /chat

The primary endpoint. Accepts a message and a conversation ID, classifies
the intent, and routes to the correct flow. Supports mixing EU AI Act
questions and compliance classifications in the same conversation.

```json
{
  "conversation_id": "abc-123",
  "message": "My AI system screens job applications and ranks candidates."
}
```

Response when a follow-up question is needed:

```json
{
  "type": "follow_up",
  "question": "Does this system make autonomous hiring decisions?"
}
```

Response for a RAG query:

```json
{
  "type": "rag_response",
  "answer": "...",
  "sources": ["Article  6", "ANNEX III"]
}
```

Response when classification is complete:

```json
{
  "type": "classification",
  "report": {
    "classification": "High risk",
    "reasoning": "...",
    "cited_articles": ["Annex III, Section 4(a)", "Article 9", "Article 14"]
  }
}
```

### POST /query

Ask a question about the EU AI Act directly, bypassing intent classification.

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

Start a compliance classification session directly, bypassing intent classification.

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

## Running evals

```bash
PYTHONPATH=. deepeval test run tests/evals/test_agent.py
```

Requires the API server to be running on port 8000.

## Why this project

This project implements each step of the RAG pipeline explicitly:
PDF parsing strategy, chunking approach, embedding model selection,
vector storage, re-ranking, retrieval, and prompt construction.

The compliance agent extends this with agentic tool use: a ReAct loop
where Claude decides which tools to call, your code executes them, and
the results feed back into the next decision. The multi-turn session
pattern is directly applicable to any agent that needs to gather
information before producing a result.

The chat layer adds intent classification and a conversation state
machine, showing how to build a unified interface over multiple distinct
AI workflows without exposing that complexity to the caller.

The EU AI Act is the domain because it is the regulatory framework that
governs AI systems in Europe. Understanding it programmatically is
directly relevant to building compliant AI applications..
