from fastapi import APIRouter
from pydantic import BaseModel
from src.retrieval.retriever import retrieve
from src.generation.generator import generate

router = APIRouter()


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    sources: list[str]


@router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Retrieve relevant chunks and generate an answer."""
    chunks = retrieve(request.question)
    result = generate(request.question, chunks)
    return QueryResponse(answer=result["answer"], sources=result["sources"])