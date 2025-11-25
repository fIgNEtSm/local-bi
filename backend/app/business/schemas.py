from pydantic import BaseModel
from uuid import UUID
from datetime import datetime as timestamp
class BusinessIn(BaseModel):
    name:UUID
    category: str
    location: str
    google_maps_url: str
    
class BusinessOut(BaseModel):
     id : str
     name:UUID
     category: str
     location: str
     google_maps_url: str
     created_at:timestamp
     

class BusinessDB(BusinessOut):
    pass
           
         