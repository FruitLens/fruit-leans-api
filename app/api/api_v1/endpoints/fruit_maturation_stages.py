from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter(prefix="/fruit-maturation-stages", tags=["fruit-maturation-stages"])


@router.get("/", response_model=List[schemas.FruitMaturationStage])
def get_all(db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100) -> Any:
    return crud.fruit_maturation_stage.get_all(db, skip=skip, limit=limit)
