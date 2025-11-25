from fastapi import APIRouter
from typing import List
from uuid import uuid4
from app.reviews.schemas import ReviewItem
from datetime import datetime

router = APIRouter(tags=["Reviews"])
reviews_db = []


@router.post("/add_batch")
def add_batch(data: List[ReviewItem]):
    for review in data:
        reviews_db.append({
            "id": str(uuid4()),
            "business_id": review.business_id,
            "reviewer_name": review.reviewer_name,
            "rating": review.rating,
            "text": review.text,
            "platform": review.platform,
            "review_date": review.review_date,
            "created_at": datetime.utcnow().isoformat()
            
        })

    return {"message": "Reviews added successfully", "count": len(data)}

