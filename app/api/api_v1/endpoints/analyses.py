from typing import Any, List, Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    Form,
    File,
    Path,
)
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
import app.crud.crud_model_predictions as model_predictions
from app.crud.upload_img_to_s3 import upload_img_to_s3

router = APIRouter(prefix="/analyses", tags=["analyses"])


@router.get("/hello", response_model=str)
def hello() -> Any:
    return "Hello darkness, my old friend... I've come to talk with you again"


@router.get("/", response_model=List[schemas.Analysis])
def get_all(db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100) -> Any:
    return crud.analysis.get_all(db, skip=skip, limit=limit)


@router.post("/predict/")
async def predict_fruit_from_image(
    *,
    db: Session = Depends(deps.get_db),
    file: Annotated[UploadFile, File()],
    telegram_img_id: Annotated[str, Form()],
    telegram_conversation_id: Annotated[str, Form()],
):
    analysis = crud.analysis.get_by_telegram_img_id(db, telegram_img_id=telegram_img_id)
    if analysis:
        raise HTTPException(
            status_code=400,
            detail=f"Analysis of telegram_img_id {telegram_img_id} already exists.",
        )

    prediction = model_predictions.predict(file)

    type_id = crud.fruit_type.get_by_name(db, name=prediction["type"]["name"]).id
    maturation_stage_id = crud.fruit_maturation_stage.get_by_name(
        db, name=prediction["maturation_stage"]["name"]
    ).id

    await upload_img_to_s3(
        file,
        f"{telegram_img_id}_{type_id}_{maturation_stage_id}.{file.filename.split('.')[-1]}",
    )

    analysis_in = schemas.AnalysisCreate(
        telegram_conversation_id=telegram_conversation_id,
        telegram_img_id=telegram_img_id,
        model_predicted_fruit_type_id=type_id,
        model_predicted_fruit_maturation_stage_id=maturation_stage_id,
    )

    crud.analysis.create(db, obj_in=analysis_in)

    return prediction


@router.put("/feedback/{telegram_img_id}")
async def update_analysis_with_user_feedback(
    *,
    db: Session = Depends(deps.get_db),
    telegram_img_id: Annotated[str, Path(title="The ID of the analysis to be updated")],
    feedback: schemas.UserFeedback,
):
    analysis = crud.analysis.get_by_telegram_img_id(db, telegram_img_id=telegram_img_id)
    if not analysis:
        raise HTTPException(
            status_code=400,
            detail=f"Analysis of telegram_img_id {telegram_img_id} does not exists.",
        )

    obj_in = {
        "user_approval": feedback.user_approval,
        "user_predicted_fruit_type_id": None,
        "user_predicted_fruit_maturation_stage_id": None,
    }

    fruit_type = crud.fruit_type.get_by_name(db, name=feedback.user_class_fruit_type)
    if not fruit_type:
        raise HTTPException(
            status_code=400,
            detail=f"FruitType of name {feedback.user_class_fruit_type} does not exists.",
        )
    obj_in["user_predicted_fruit_type_id"] = fruit_type.id

    if feedback.user_class_maturation_stage:
        maturation_stage = crud.fruit_maturation_stage.get_by_name(
            db, name=feedback.user_class_maturation_stage
        )
        if not maturation_stage:
            raise HTTPException(
                status_code=400,
                detail=f"FruitMaturationStage of name {feedback.user_class_maturation_stage} does not exists.",
            )
        obj_in["user_predicted_fruit_maturation_stage_id"] = maturation_stage.id

    updated = crud.analysis.update(
        db,
        db_obj=analysis,
        obj_in=obj_in,
    )
    return updated
