from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.app.services.onboarding_service import onboarding_service


router = APIRouter(prefix="/api/v1/onboarding", tags=["Type 1 - Onboarding"])


class IndexRequest(BaseModel):
    project_path: str


class QueryRequest(BaseModel):
    question: str


@router.post("/index")
def index_codebase(request: IndexRequest):
    try:
        return onboarding_service.index_project(request.project_path)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.get("/architecture-summary")
def get_architecture_summary():
    try:
        return onboarding_service.architecture_summary()
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error


@router.post("/ask-copilot")
def ask_copilot(payload: QueryRequest):
    if not payload.question.strip():
        raise HTTPException(status_code=422, detail="Question cannot be empty")
    if onboarding_service.project_path is None:
        raise HTTPException(status_code=409, detail="Index a codebase before asking questions")
    snippets = onboarding_service.search(payload.question)
    return {
        "answer": "Relevant code was retrieved from the indexed codebase.",
        "snippets": snippets,
        "match_count": len(snippets),
    }