from pydantic import BaseModel, Field
from typing import List, Optional

class CompletionRequest(BaseModel):
    text: str = Field(..., description="The text context for generating completions")
    max_suggestions: Optional[int] = Field(default=3, description="Maximum number of suggestions to return")
    context_type: Optional[str] = Field(default="paragraph", description="Type of context (paragraph, claim, section)")

class CompletionResponse(BaseModel):
    suggestions: List[str] = Field(..., description="List of generated suggestions")
    confidence: float = Field(..., description="Confidence score for the suggestions")
    processing_time_ms: int = Field(..., description="Time taken to process the request")
    rules_applied: List[str] = Field(default=[], description="List of rules applied during generation") 