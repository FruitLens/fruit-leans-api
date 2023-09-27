from .crud_analysis import analysis
from .crud_fruit_type import fruit_type
from .crud_fruit_maturation_stage import fruit_maturation_stage

# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
