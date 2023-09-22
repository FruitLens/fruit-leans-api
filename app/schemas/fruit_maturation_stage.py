from pydantic import BaseModel


# Shared properties
class FruitMaturationStageBase(BaseModel):
    name: str = None


# Properties to receive on fruit_maturation_stage creation
class FruitMaturationStageCreate(FruitMaturationStageBase):
    pass


# Properties to receive on fruit_maturation_stage update
class FruitMaturationStageUpdate(FruitMaturationStageBase):
    pass


# Properties shared by models stored in DB
class FruitMaturationStageInDBBase(FruitMaturationStageBase):
    id: int
    name: str

    class Config:
        orm_mode = True


# Properties to return to client
class FruitMaturationStage(FruitMaturationStageInDBBase):
    pass


# Properties properties stored in DB
class FruitMaturationStageInDB(FruitMaturationStageInDBBase):
    pass
