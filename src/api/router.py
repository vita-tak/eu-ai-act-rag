import uuid
import asyncio
from fastapi.concurrency import run_in_threadpool
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.retrieval.retriever import retrieve
from src.generation.generator import generate
from src.agent.agent import run_agent

router = APIRouter()

# In-memory session store: session_id -> messages list.
sessions = {}


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    sources: list[str]


class ClassifyRequest(BaseModel):
    product_description: str


class AnswerRequest(BaseModel):
    session_id: str
    answer: str


class ClassifyResponse(BaseModel):
    status: str
    session_id: str | None = None
    question: str | None = None
    classification: str | None = None
    reasoning: str | None = None
    cited_articles: list[str] | None = None


@router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    chunks = retrieve(request.question)
    result = generate(request.question, chunks)
    return QueryResponse(answer=result["answer"], sources=result["sources"])


@router.post("/classify/start", response_model=ClassifyResponse)
async def classify_start(request: ClassifyRequest):
    session_id = str(uuid.uuid4())
    messages = [
        {"role": "user", "content": request.product_description}
    ]

    result = await run_in_threadpool(run_agent, messages)
    sessions[session_id] = result["messages"]

    if result["status"] == "follow_up":
        return ClassifyResponse(
            status="follow_up",
            session_id=session_id,
            question=result["question"]
        )

    return ClassifyResponse(
        status="done",
        session_id=session_id,
        classification=result["report"]["classification"],
        reasoning=result["report"]["reasoning"],
        cited_articles=result["report"]["cited_articles"]
    )


@router.post("/classify/answer", response_model=ClassifyResponse)
async def classify_answer(request: AnswerRequest):
    if request.session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    messages = sessions[request.session_id]
    messages.append({"role": "user", "content": request.answer})

    result = await run_in_threadpool(run_agent, messages)
    sessions[request.session_id] = result["messages"]

    if result["status"] == "follow_up":
        return ClassifyResponse(
            status="follow_up",
            session_id=request.session_id,
            question=result["question"]
        )

    return ClassifyResponse(
        status="done",
        session_id=request.session_id,
        classification=result["report"]["classification"],
        reasoning=result["report"]["reasoning"],
        cited_articles=result["report"]["cited_articles"]
    )