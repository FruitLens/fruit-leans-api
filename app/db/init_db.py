from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings
from app.db.base import Base


# from app.db.session import engine

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    fruit_types_names = ["APPLE", "BANANA", "ORANGE"]

    for f_name in fruit_types_names:
        fruit_type = crud.fruit_type.get_by_name(db, name=f_name)
        if fruit_type is None:
            fruit_type_in = schemas.FruitTypeCreate(name=f_name)
            crud.fruit_type.create(db, obj_in=fruit_type_in)
