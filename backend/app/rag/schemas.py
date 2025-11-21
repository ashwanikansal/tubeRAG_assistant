from pydantic import BaseModel

class ChatRequest(BaseModel):
    video_id_or_url: str
    question: str

class ChatResponse(BaseModel):
    video_id: str
    answer: str
