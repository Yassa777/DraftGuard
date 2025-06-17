from fastapi import APIRouter, HTTPException
from ...schemas.schemas import CompletionRequest, CompletionResponse
from ...services.completion_service import CompletionService

router = APIRouter()

@router.post("/completions", response_model=CompletionResponse)
async def get_completions(request: CompletionRequest):
    try:
        return await CompletionService.get_completions(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 