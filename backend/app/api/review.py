from fastapi import APIRouter, HTTPException

from backend.Agent1.security_quality_agent import security_quality_agent
from backend.app.models.review import ReviewRequest, ReviewResponse


router = APIRouter(prefix="/api/v1", tags=["Type 2 - PR Review"])


@router.post("/review", response_model=ReviewResponse)
def review_code(request: ReviewRequest):
    try:
        return security_quality_agent.review(request.code, request.language)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error