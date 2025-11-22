from pydantic import BaseModel
from typing import List

class ReviewItem(BaseModel):
    rating: float
    text: str
    date: str

class ReviewBatch(BaseModel):
    business_id: int
    reviews: List[ReviewItem]
