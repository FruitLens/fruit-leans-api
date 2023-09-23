from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter(prefix="/analyses", tags=["analyses"])


@router.get("/", response_model=str)
def hello() -> Any:
    return "Hello darkness, my old friend... I've come to talk with you again"
