from pydantic import BaseModel
from uuid import UUID
from datetime import datetime as timestamp
from typing import Optional,Dict,Any

class TrendsIn(BaseModel): 
    business_id:UUID
    week:int
    month:int
    sentiment_score:float
    topic_trends:Dict[str,Any]
    
    
class TrendsOut(TrendsIn):
    id:UUID
    created_at:timestamp
    

