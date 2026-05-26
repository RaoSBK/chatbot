from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Recommendation_schemaBase(BaseModel):
    pass

class Recommendation_schemaCreate(Recommendation_schemaBase):
    pass

class Recommendation_schema(Recommendation_schemaBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
