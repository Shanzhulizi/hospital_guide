from pydantic import BaseModel

class ChatRequest(BaseModel):
    type: str  # 'symptom' | 'navigate' | 'qa'
    input: str
