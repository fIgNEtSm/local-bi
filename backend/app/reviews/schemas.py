from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ReviewItem(BaseModel):
    business_id : str
    reviewer_name: Optional[str] = None
    rating: int
    text: str
    platform: str           
    review_date: datetime   

class ReviewBatch(BaseModel):
    id: str
    reviews: List[ReviewItem]
    created_at: datetime
