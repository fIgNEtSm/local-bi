from pydantic import BaseModel

class BusinessIn(BaseModel):
    name: str
    address: str
    category: str
    google_maps_url: str
