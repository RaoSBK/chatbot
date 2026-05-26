from fastapi import APIRouter, Depends, HTTPException
from typing import List

router = APIRouter(
    prefix="/alerts",
    tags=["alerts"]
)

@router.get("/")
async def get_all():
    return {"message": "Get all from alerts"}

@router.get("/{id}")
async def get_by_id(id: int):
    return {"message": f"Get item {id} from alerts"}
