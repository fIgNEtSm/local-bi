from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import  List


class AIRequest(BaseModel):
    business_id: UUID


class AIAnalysisIn(BaseModel):
    sentiment_pos: int
    sentiment_neg: int
    sentiment_neu: int
    top_topics: dict
    keywords: List[str] 
    top_complaints: List[str] 
    top_praises: List[str] 
    ai_insights: str


class AIAnalysisOut(AIAnalysisIn):
    id: UUID
    updated_at: datetime