from fastapi import APIRouter, Depends, HTTPException
from typing import List

router = APIRouter(
    prefix="/budgets",
    tags=["budgets"]
)

@router.get("/")
async def get_all():
    return {"message": "Get all from budgets"}

@router.get("/{id}")
async def get_by_id(id: int):
    return {"message": f"Get item {id} from budgets"}
