from fastapi import APIRouter, HTTPException
from app.business.schemas import BusinessIn

router = APIRouter(tags=["Business"])

fake_business_db = []

@router.post("/register")
def register_business(data: BusinessIn):
    fake_business_db.append(data.dict())
    return {"message": "Business registered successfully"}

