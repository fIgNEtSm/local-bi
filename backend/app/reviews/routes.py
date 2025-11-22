from fastapi import APIRouter
from app.reviews.schemas import ReviewBatch

router = APIRouter(tags=["Reviews"])

fake_reviews_db = []

@router.post("/add")
def add_reviews(batch: ReviewBatch):
    for review in batch.reviews:
        fake_reviews_db.append({
            "business_id": batch.business_id,
            "rating": review.rating,
            "text": review.text,
            "date": review.date
        })
    return {"message": "Reviews added", "count": len(batch.reviews)}
