from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.fruit_type import FruitType
from app.schemas.fruit_type import FruitTypeCreate, FruitTypeUpdate


class CRUDFruitType(CRUDBase[FruitType, FruitTypeCreate, FruitTypeUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[FruitType]:
        return db.query(FruitType).filter(FruitType.name == name).first()

    def create(self, db: Session, *, obj_in: FruitTypeCreate) -> FruitType:
        db_obj = FruitType(name=obj_in.name)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


fruit_type = CRUDFruitType(FruitType)
