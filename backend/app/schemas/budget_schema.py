from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Budget_schemaBase(BaseModel):
    pass

class Budget_schemaCreate(Budget_schemaBase):
    pass

class Budget_schema(Budget_schemaBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
