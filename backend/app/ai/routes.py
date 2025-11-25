from fastapi import APIRouter, HTTPException
from app.ai.schemas import AIAnalysisIn, AIAnalysisOut, AIRequest
from app.reviews.routes import reviews_db
from uuid import UUID
from datetime import datetime

router = APIRouter(tags=["AI Analysis"])

ai_db = {}

@router.post("/update/{business_id}")
def update_ai(business_id: UUID, data: AIRequest):
    # Simulate AI analysis process
    ai_db[business_id] = {
        "id": str(UUID()),
        "business_id": business_id,
        **data.dict(),
        "updated_at": datetime.utcnow()
    }
    
    return ai_db[business_id]

@router.get("/{business_id}", response_model=AIAnalysisOut)
def get_ai(business_id: UUID):
    return ai_db[business_id]