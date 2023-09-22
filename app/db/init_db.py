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
    fruit_maturation_stages_names = ["RAW", "UNRIPE", "RIPE", "OVERRIPE", "ROTTEN"]

    for f_name in fruit_types_names:
        fruit_type = crud.fruit_type.get_by_name(db, name=f_name)
        if fruit_type is None:
            fruit_type_in = schemas.FruitTypeCreate(name=f_name)
            crud.fruit_type.create(db, obj_in=fruit_type_in)

    for f_name in fruit_maturation_stages_names:
        fruit_maturation_stage = crud.fruit_maturation_stage.get_by_name(
            db, name=f_name
        )
        if fruit_maturation_stage is None:
            fruit_maturation_stage_in = schemas.FruitMaturationStageCreate(name=f_name)
            crud.fruit_maturation_stage.create(db, obj_in=fruit_maturation_stage_in)
