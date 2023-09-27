from typing import List, Optional

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


analysis = CRUDAnalysis(Analysis)
