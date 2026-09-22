from fastapi import APIRouter, HTTPException
from backend.indexing_agent import IndexingAgent
from backend.app.models.codebase import CodebaseIndexRequest, CodebaseIndexResponse

router = APIRouter(prefix="/api/v1/codebase", tags=["Codebase"])
indexing_agent = IndexingAgent()


@router.post("/index", response_model=CodebaseIndexResponse)
def index_codebase(request: CodebaseIndexRequest):
    try:
        return indexing_agent.index_project(request.project_path)
    except (FileNotFoundError, ValueError) as error:
        raise HTTPException(status_code=400, detail=str(error)) from error