from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String

from app.db.base_class import Base

if TYPE_CHECKING:
    from .item import Item  # noqa: F401


class FruitMaturationStage(Base):
    __tablename__ = "fruit_maturation_stage"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"FruitMaturationStage(id={self.id!r}, name={self.name!r})"
