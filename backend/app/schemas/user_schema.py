from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class User_schemaBase(BaseModel):
    pass

class User_schemaCreate(User_schemaBase):
    pass

class User_schema(User_schemaBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
