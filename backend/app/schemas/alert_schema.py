from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Alert_schemaBase(BaseModel):
    pass

class Alert_schemaCreate(Alert_schemaBase):
    pass

class Alert_schema(Alert_schemaBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
