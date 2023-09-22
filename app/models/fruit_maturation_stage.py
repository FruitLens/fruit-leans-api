# from typing import TYPE_CHECKING
#
# from sqlalchemy import Boolean, Column, Integer, String
# from sqlalchemy.orm import relationship
#
# from app.db.base_class import Base
#
# if TYPE_CHECKING:
#     from .item import Item  # noqa: F401
#
#
# class FruitMaturationStage(Base):
#     __tablename__ = "fruit_maturation_stage"
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#
#     # predicted_analyses = relationship(
#     #     "Analysis", back_populates="predicted_fruit_maturation_stage"
#     # )
#     # user_analyses = relationship(
#     #     "Analysis", back_populates="user_fruit_maturation_stage"
#     # )
#
#     def __repr__(self):
#         return f"FruitMaturationStage(id={self.id!r}, name={self.name!r})"
