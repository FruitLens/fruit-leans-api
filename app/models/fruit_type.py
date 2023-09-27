from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .item import Item  # noqa: F401


class FruitType(Base):
    __tablename__ = "fruit_type"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    model_predicted_analyses = relationship(
        "Analysis",
        foreign_keys="Analysis.model_predicted_fruit_type_id",
        back_populates="model_predicted_fruit_type",
    )
    user_predicted_analyses = relationship(
        "Analysis",
        foreign_keys="Analysis.user_predicted_fruit_type_id",
        back_populates="user_predicted_fruit_type",
    )

    def __repr__(self):
        return f"FruitType(id={self.id!r}, name={self.name!r})"
