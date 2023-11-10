from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, ForeignKey, Boolean, Text, String, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Analysis(Base):
    __tablename__ = "analysis"
    id = Column(Integer, primary_key=True)
    telegram_img_id = Column(String, unique=True, nullable=False)
    telegram_conversation_id = Column(String, nullable=False)

    model_predicted_fruit_type_id = Column(Integer, ForeignKey("fruit_type.id"))
    user_predicted_fruit_type_id = Column(Integer, ForeignKey("fruit_type.id"))

    model_fruit_type_name = Column(String, nullable=False, server_default="UNKNOWN")
    model_fruit_stage_name = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    model_predicted_fruit_type = relationship(
        "FruitType",
        foreign_keys=model_predicted_fruit_type_id,
        back_populates="model_predicted_analyses",
    )
    user_predicted_fruit_type = relationship(
        "FruitType",
        foreign_keys=user_predicted_fruit_type_id,
        back_populates="user_predicted_analyses",
    )

    model_predicted_fruit_maturation_stage_id = Column(
        Integer, ForeignKey("fruit_maturation_stage.id")
    )
    user_predicted_fruit_maturation_stage_id = Column(
        Integer, ForeignKey("fruit_maturation_stage.id")
    )

    model_predicted_fruit_maturation_stage = relationship(
        "FruitMaturationStage",
        foreign_keys=model_predicted_fruit_maturation_stage_id,
        back_populates="model_predicted_analyses",
    )
    user_predicted_fruit_maturation_stage = relationship(
        "FruitMaturationStage",
        foreign_keys=user_predicted_fruit_maturation_stage_id,
        back_populates="user_predicted_analyses",
    )

    user_approval = Column(Boolean)

    def __repr__(self):
        return f"Analysis(id={self.id!r})"
