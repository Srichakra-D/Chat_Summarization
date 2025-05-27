from pydantic import BaseModel

class SummarizationRequest(BaseModel):
    conversation_id: str

class SummaryResponse(BaseModel):
    conversation_id: str
    summary_text: str