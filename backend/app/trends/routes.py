from fastapi import APIRouter,HTTPException
from uuid import UUID
from datetime import datetime
from app.trends.schemas import TrendsOut

router = APIRouter(tags=["Trends"])


@router.get("/{business_id}", response_model=TrendsOut)
def get_trends(business_id: UUID):
    # Example static response — in real code replace with DB lookup
    return {
        "id": UUID("123e4567-e89b-12d3-a456-426614174000"),
        "business_id": business_id,
        "week": 34,
        "month": 8,
        "sentiment_score": 0.75,
        "topic_trends": {"topic1": "up", "topic2": "down"},
        "created_at": "2024-08-21T12:34:56Z"
    }