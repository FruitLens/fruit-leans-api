from typing import List, Optional, Union, Dict, Any

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.analysis import Analysis
from app.schemas.analysis import AnalysisCreate, AnalysisUpdate


class CRUDAnalysis(CRUDBase[Analysis, AnalysisCreate, AnalysisUpdate]):
    def get_all(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Analysis]:
        return db.query(Analysis).offset(skip).limit(limit).all()

    def get_by_telegram_img_id(
        self, db: Session, *, telegram_img_id: str
    ) -> Optional[Analysis]:
        return (
            db.query(Analysis)
            .filter(Analysis.telegram_img_id == telegram_img_id)
            .first()
        )

    def update(
        self,
        db: Session,
        *,
        db_obj: Analysis,
        obj_in: Union[AnalysisUpdate, Dict[str, Any]]
    ) -> Analysis:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


analysis = CRUDAnalysis(Analysis)
