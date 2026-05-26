from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Goal_schemaBase(BaseModel):
    pass

class Goal_schemaCreate(Goal_schemaBase):
    pass

class Goal_schema(Goal_schemaBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
