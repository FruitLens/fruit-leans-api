from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.fruit_maturation_stage import FruitMaturationStage
from app.schemas.fruit_maturation_stage import (
    FruitMaturationStageCreate,
    FruitMaturationStageUpdate,
)


class CRUDFruitMaturationStage(
    CRUDBase[
        FruitMaturationStage, FruitMaturationStageCreate, FruitMaturationStageUpdate
    ]
):
    def get_all(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[FruitMaturationStage]:
        return db.query(FruitMaturationStage).offset(skip).limit(limit).all()

    def get_by_name(self, db: Session, *, name: str) -> Optional[FruitMaturationStage]:
        return (
            db.query(FruitMaturationStage)
            .filter(FruitMaturationStage.name == name)
            .first()
        )

    def create(
        self, db: Session, *, obj_in: FruitMaturationStageCreate
    ) -> FruitMaturationStage:
        db_obj = FruitMaturationStage(name=obj_in.name)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


fruit_maturation_stage = CRUDFruitMaturationStage(FruitMaturationStage)
