from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter(prefix="/analyses", tags=["analyses"])


@router.get("/hello", response_model=str)
def hello() -> Any:
    return "Hello darkness, my old friend... I've come to talk with you again"


@router.get("/", response_model=List[schemas.Analysis])
def get_all(db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100) -> Any:
    return crud.analysis.get_all(db, skip=skip, limit=limit)


@router.post("/", response_model=schemas.Analysis)
def create_analysis(
        *, db: Session = Depends(deps.get_db), analysis_in: schemas.AnalysisCreate
) -> Any:
    """
    Create new analysis.
    """
    analysis = crud.analysis.get_by_telegram_img_id(
        db, telegram_img_id=analysis_in.telegram_img_id
    )
    if analysis:
        raise HTTPException(
            status_code=400,
            detail=f"The analysis of image {analysis_in.telegram_img_id} already exists.",
        )

    return crud.analysis.create(db, obj_in=analysis_in)
