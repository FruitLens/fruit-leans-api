from typing import Union

from pydantic import BaseModel


# class FruitTypeBase(BaseModel):
#     name: str
#
#
# class FruitTypeCreate(FruitTypeBase):
#     pass


# class FruitType(FruitTypeBase):
#     id: int
#     # analyses: list[Analysis] = []
#
#     class Config:
#         orm_mode = True


class FruitType(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class FruitMaturationStageBase(BaseModel):
    name: str


class FruitMaturationStageCreate(FruitMaturationStageBase):
    pass


class FruitMaturationStage(FruitMaturationStageBase):
    id: int
    # analyses: list[Analysis] = []

    class Config:
        orm_mode = True


# class AnalysisBase(BaseModel):
#     telegram_conversation_id: str
#     telegram_image_id: str

#     predicted_fruit_type_id: Union[str, None] = None
#     predicted_fruit_maturation_stage_id: Union[str, None] = None

#     user_approval: Union[bool, None] = None
#     user_message: Union[str, None] = None
#     user_classification: Union[str, None] = None


# class Analysis(AnalysisBase):
#     id: int
#     fruit_type: Union[FruitType, None] = None
#     fruit_maturation_stage: Union[FruitMaturationStage, None] = None

#     class Config:
#         orm_mode = True
