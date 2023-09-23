from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter(prefix="/fruit-types", tags=["fruit-types"])


@router.get("/", response_model=List[schemas.FruitType])
def get_all(db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100) -> Any:
    return crud.fruit_type.get_all(db, skip=skip, limit=limit)
