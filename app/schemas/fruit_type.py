from typing import Optional

from pydantic import BaseModel


# Shared properties
class FruitTypeBase(BaseModel):
    name: str = None
    # title: Optional[str] = None
    # description: Optional[str] = None


# Properties to receive on fruit_type creation
class FruitTypeCreate(FruitTypeBase):
    # title: str
    pass


# Properties to receive on fruit_type update
class FruitTypeUpdate(FruitTypeBase):
    pass


# Properties shared by models stored in DB
class FruitTypeInDBBase(FruitTypeBase):
    id: int
    name: str
    # owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class FruitType(FruitTypeInDBBase):
    pass


# Properties properties stored in DB
class FruitTypeInDB(FruitTypeInDBBase):
    pass
