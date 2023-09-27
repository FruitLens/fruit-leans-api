from typing import Optional

from pydantic import BaseModel


# Shared properties
class AnalysisBase(BaseModel):
    telegram_img_id: str
    telegram_conversation_id: str
    model_predicted_fruit_type_id: int
    model_predicted_fruit_maturation_stage_id: Optional[int]


# Properties to receive on fruit_maturation_stage creation
class AnalysisCreate(AnalysisBase):
    pass


# Properties to receive on fruit_maturation_stage update
class AnalysisUpdate(AnalysisBase):
    pass


# Properties shared by models stored in DB
class AnalysisInDBBase(AnalysisBase):
    id: int
    user_predicted_fruit_type_id: Optional[int]

    user_predicted_fruit_maturation_stage_id: Optional[int]

    user_approval: Optional[bool]

    class Config:
        orm_mode = True


# Properties to return to client
class Analysis(AnalysisInDBBase):
    pass


# Properties stored in DB
class AnalysisInDB(AnalysisInDBBase):
    pass
