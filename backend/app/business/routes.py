from fastapi import APIRouter, HTTPException
from uuid import UUID
from datetime import datetime   
from app.business.schemas import BusinessIn

router = APIRouter(tags=["Business"])

business_db = []

@router.post("/register")
def register_business(data: BusinessIn):
    new_business ={
        "id": str(UUID()),
        "name": data.name,
        "category": data.category,
        "location": data.location,
        "google_maps_url": data.google_maps_url,
        "created_at": datetime.utcnow()
    }
    
    business_db.append(new_business)
    return new_business