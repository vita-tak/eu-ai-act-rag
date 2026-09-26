# EU AI Act Compliace Assistant (Agentic RAG system)

An agentic RAG system with chat interface designed to query the EU AI Act in natural language and determine the risk category of an AI system under the regulation.

**Live:** [assistant.sarek.technology](https://assistant.sarek.technology)

## What it does

Ask questions about the EU AI Act in natural language, or describe an AI system to get a risk classification. The agent asks follow-up questions when it needs more information and produces a structured report with classification, reasoning, and cited articles.

## Tech stack

| Component         | Technology                              |
| ----------------- | --------------------------------------- |
| Frontend          | Next.js, TypeScript, Tailwind CSS       |
| API               | FastAPI, Python 3.12                    |
| LLM               | Claude Haiku (Anthropic)                |
| Embeddings        | OpenAI text-embedding-3-small           |
| Vector database   | Chroma                                  |
| Re-ranking        | sentence-transformers CrossEncoder      |
| PDF parsing       | Docling (local build-time only)         |

## Project structure

```
eu-ai-act-rag/
├── ai-service/          # FastAPI backend
│   ├── src/
│   │   ├── rag/         # ingestion, retrieval, generation
│   │   ├── agent/       # ReAct loop and tools
│   │   ├── chat/        # intent classifier and conversation state
│   │   ├── middleware/  # CORS and rate limiting
│   │   └── api/         # FastAPI app and router
│   ├── tests/evals/     # DeepEval agent evals
│   └── main.py          # CLI entry point
└── frontend/            # Next.js chat interface
```

## Running locally

### Prerequisites

Python 3.12+, Node.js, Bun, Anthropic API key, OpenAI API key

### Backend

```bash
cd ai-service
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add ANTHROPIC_API_KEY and OPENAI_API_KEY to .env
PYTHONPATH=. uvicorn src.api.app:app --reload
```

The Chroma database is included in the repo and ready to use. API docs at `http://localhost:8000/docs`.

### Frontend

```bash
cd frontend
bun install
bun dev
```

Open `http://localhost:3000`.

## API

### POST /chat

```json
{ "conversation_id": "abc-123", "message": "My AI system screens job applications." }
```

Returns one of three response types:

```json
{ "type": "rag_response", "answer": "...", "sources": ["Article 6", "ANNEX III"] }
{ "type": "follow_up", "question": "Does the system make autonomous hiring decisions?" }
{ "type": "classification", "report": { "classification": "High risk", "reasoning": "...", "cited_articles": ["..."] } }
```

## Running evals

```bash
cd ai-service
PYTHONPATH=. deepeval test run tests/evals/test_agent.py
```

Requires the API server to be running.
