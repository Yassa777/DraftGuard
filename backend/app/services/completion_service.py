import time
from typing import List
from ..schemas.schemas import CompletionRequest, CompletionResponse

class CompletionService:
    @staticmethod
    async def get_completions(request: CompletionRequest) -> CompletionResponse:
        # Simulate processing time
        start_time = time.time()
        
        # Mock suggestions based on context type
        suggestions = []
        if request.context_type == "claim":
            suggestions = [
                "wherein the apparatus further comprises a processor configured to...",
                "wherein the method further includes the step of...",
                "wherein the system is configured to..."
            ]
        else:
            suggestions = [
                "The present invention relates to...",
                "In accordance with one embodiment...",
                "It is an object of the present invention to..."
            ]
        
        # Limit suggestions based on max_suggestions
        suggestions = suggestions[:request.max_suggestions]
        
        # Calculate processing time
        processing_time = int((time.time() - start_time) * 1000)
        
        return CompletionResponse(
            suggestions=suggestions,
            confidence=0.85,
            processing_time_ms=processing_time,
            rules_applied=["USPTO_CLAIM_FORMAT", "ANTECEDENT_BASIS"]
        ) 