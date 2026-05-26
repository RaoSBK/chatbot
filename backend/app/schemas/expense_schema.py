from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Expense_schemaBase(BaseModel):
    pass

class Expense_schemaCreate(Expense_schemaBase):
    pass

class Expense_schema(Expense_schemaBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
