from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from uuid import UUID

import database as crud
from database import SessionLocal, init_db

from pydantic import BaseModel

# -------------------------------------------------
# APP INITIALIZATION
# -------------------------------------------------

app = FastAPI(title="Business Intelligence API")

@app.on_event("startup")
def startup():
    init_db()

# -------------------------------------------------
# DATABASE DEPENDENCY
# -------------------------------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------------------------------
# Pydantic Schemas
# -------------------------------------------------

# -------- BUSINESS --------
class BusinessCreate(BaseModel):
    name: str
    category: Optional[str] = None
    location: Optional[str] = None
    google_maps_url: Optional[str] = None

class BusinessUpdate(BaseModel):
    name: Optional[str]
    category: Optional[str]
    location: Optional[str]
    google_maps_url: Optional[str]

class BusinessOut(BusinessCreate):
    id: UUID

    class Config:
        from_attributes = True


# -------- REVIEWS --------
class ReviewCreate(BaseModel):
    business_id: UUID
    reviewer_name: Optional[str]
    rating: int
    text: Optional[str]
    platform: Optional[str]
    review_date: datetime

class ReviewOut(ReviewCreate):
    id: UUID

    class Config:
        from_attributes = True


# -------- TREND LOG --------
class TrendLogCreate(BaseModel):
    business_id: UUID
    week: Optional[int]
    month: Optional[int]
    sentiment_score: Optional[float]
    topic_trends: Optional[dict]

class TrendLogOut(TrendLogCreate):
    id: UUID

    class Config:
        from_attributes = True


# -------- AI RESULT --------
class AIResultCreate(BaseModel):
    sentiment_pos: Optional[int]
    sentiment_neg: Optional[int]
    sentiment_neu: Optional[int]
    top_topics: Optional[dict]
    keywords: Optional[dict]
    top_complaints: Optional[dict]
    top_praises: Optional[dict]
    ai_insights: Optional[str]

class AIResultOut(AIResultCreate):
    id: UUID
    business_id: UUID

    class Config:
        from_attributes = True


# -------------------------------------------------
# BUSINESS ENDPOINTS
# -------------------------------------------------

@app.post("/businesses", response_model=BusinessOut)
def create_business(data: BusinessCreate, db: Session = Depends(get_db)):
    return crud.create_business(
        db, data.name, data.category, data.location, data.google_maps_url
    )

@app.get("/businesses", response_model=List[BusinessOut])
def list_businesses(db: Session = Depends(get_db)):
    return crud.list_businesses(db)

@app.get("/businesses/{business_id}", response_model=BusinessOut)
def get_business(business_id: UUID, db: Session = Depends(get_db)):
    business = crud.get_business(db, business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    return business

@app.put("/businesses/{business_id}", response_model=BusinessOut)
def update_business(business_id: UUID, data: BusinessUpdate, db: Session = Depends(get_db)):
    business = crud.update_business(db, business_id, data.dict(exclude_unset=True))
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    return business

@app.delete("/businesses/{business_id}")
def delete_business(business_id: UUID, db: Session = Depends(get_db)):
    success = crud.delete_business(db, business_id)
    if not success:
        raise HTTPException(status_code=404, detail="Business not found")
    return {"deleted": True}


# -------------------------------------------------
# REVIEW ENDPOINTS
# -------------------------------------------------

@app.post("/reviews", response_model=ReviewOut)
def create_review(data: ReviewCreate, db: Session = Depends(get_db)):
    return crud.create_review(
        db,
        data.business_id,
        data.reviewer_name,
        data.rating,
        data.text,
        data.platform,
        data.review_date,
    )

@app.get("/reviews/{business_id}", response_model=List[ReviewOut])
def get_reviews(business_id: UUID, db: Session = Depends(get_db)):
    return crud.get_reviews_by_business(db, business_id)

@app.delete("/reviews/{review_id}")
def delete_review(review_id: UUID, db: Session = Depends(get_db)):
    success = crud.delete_review(db, review_id)
    if not success:
        raise HTTPException(status_code=404, detail="Review not found")
    return {"deleted": True}


# -------------------------------------------------
# TREND LOG ENDPOINTS
# -------------------------------------------------

@app.post("/trends", response_model=TrendLogOut)
def create_trend_log(data: TrendLogCreate, db: Session = Depends(get_db)):
    return crud.create_trend_log(
        db,
        data.business_id,
        data.week,
        data.month,
        data.sentiment_score,
        data.topic_trends,
    )

@app.get("/trends/{business_id}", response_model=List[TrendLogOut])
def get_trend_logs(business_id: UUID, db: Session = Depends(get_db)):
    return crud.get_trend_logs(db, business_id)

@app.delete("/trends/{log_id}")
def delete_trend_log(log_id: UUID, db: Session = Depends(get_db)):
    success = crud.delete_trend_log(db, log_id)
    if not success:
        raise HTTPException(status_code=404, detail="Trend log not found")
    return {"deleted": True}


# -------------------------------------------------
# AI RESULT ENDPOINTS
# -------------------------------------------------

@app.post("/ai-results/{business_id}", response_model=AIResultOut)
def save_ai_result(business_id: UUID, data: AIResultCreate, db: Session = Depends(get_db)):
    return crud.save_ai_result(db, business_id, data.dict())

@app.get("/ai-results/{business_id}", response_model=AIResultOut)
def get_ai_result(business_id: UUID, db: Session = Depends(get_db)):
    result = crud.get_ai_results(db, business_id)
    if not result:
        raise HTTPException(status_code=404, detail="AI result not found")
    return result
