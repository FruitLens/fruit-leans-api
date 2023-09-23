# import io
# import os
# import boto3
#
# import numpy as np
# import tensorflow as tf
# from fastapi import Depends, FastAPI, HTTPException, UploadFile
# from sqlalchemy.orm import Session
#
# from . import crud, models, schemas
# from .database import SessionLocal, engine

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings


app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)


# # outside docker
# identification_model = tf.keras.models.load_model(
#     os.path.join("models", "fruit_type_classifier_v2.h5")
# )
# stages_model = tf.keras.models.load_model(
#     os.path.join("models", "banana_stages_classifier_v3.h5")
# )


# inside docker
# identification_model = tf.keras.models.load_model(os.path.join("./fruit_type_classifier_v2.h5"))
# banana_stages_model = tf.keras.models.load_model(os.path.join("./banana_stages_classifier_v3.h5"))


# @app.get("/")
# async def root():
#     return "FruitLens API"
#
#
# @app.post("/predict/fruit")
# async def predict_fruit_from_image(file: UploadFile):
#     img = io.BytesIO(file.file.read())
#
#     img_array = __image_to_image_array(img)
#
#     fruit_type_class, fruit_type_confidence = predict_identification(img_array)
#     fruit_stage_class, fruit_stage_confidence = None, None
#
#     if fruit_type_class == "BANANA":
#         fruit_stage_class, fruit_stage_confidence = predict_stages(img_array)
#
#     return {
#         "type": {"name": fruit_type_class, "confidence": fruit_type_confidence},
#         "stage": {"name": fruit_stage_class, "confidence": fruit_stage_confidence},
#     }
#
#
# @app.post("/upload")
# async def upload_file_to_s3(file: UploadFile, file_name: str):
#     try:
#         s3 = boto3.client("s3")
#         s3.put_object(
#             Bucket=S3_S3_BUCKET_NAME, Key="users_images/" + file_name, Body=file.file
#         )
#     except Exception as e:
#         print(e)
#         return False
#     return True
#
#
# @app.get("/fruit-types", response_model=list[schemas.FruitType])
# def get_fruit_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     fruit_types = crud.get_fruit_types(db, skip=skip, limit=limit)
#     return fruit_types
#
#
# def __image_to_image_array(img_path):
#     img = tf.keras.utils.load_img(
#         img_path, target_size=(CLASSIFICATION_IMG_HEIGHT, CLASSIFICATION_IMG_WIDTH)
#     )
#
#     img_array = tf.keras.utils.img_to_array(img)
#     img_array = tf.expand_dims(img_array, 0)
#
#     return img_array
#
#
# def predict_identification(img_array):
#     predictions = identification_model.predict(img_array, verbose=False)
#     score = tf.nn.softmax(predictions[0])

# _type = FRUIT_TYPE_CLASS_NAMES[np.argmax(score)]
# confidence = 100 * np.max(score)

# @app.post("/predict/fruit")
# async def predict_fruit_from_image(file: UploadFile):
#     img = io.BytesIO(file.file.read())
#
#     img_array = __image_to_image_array(img)
#
#     fruit_type_class, fruit_type_confidence = predict_identification(img_array)
#     fruit_stage_class, fruit_stage_confidence = None, None
#
#     if fruit_type_class == "BANANA":
#         fruit_stage_class, fruit_stage_confidence = predict_stages(img_array)
#
#     return {
#         "type": {"name": fruit_type_class, "confidence": fruit_type_confidence},
#         "stage": {"name": fruit_stage_class, "confidence": fruit_stage_confidence},
#     }
#
#
# @app.post("/upload")
# async def upload_file_to_s3(file: UploadFile, file_name: str):
#     try:
#         s3 = boto3.client("s3")
#         s3.put_object(
#             Bucket=S3_S3_BUCKET_NAME, Key="users_images/" + file_name, Body=file.file
#         )
#     except Exception as e:
#         print(e)
#         return False
#     return True
#
#
# @app.get("/fruit-types", response_model=list[schemas.FruitType])
# def get_fruit_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     fruit_types = crud.get_fruit_types(db, skip=skip, limit=limit)
#     return fruit_types
#
#
# def __image_to_image_array(img_path):
#     img = tf.keras.utils.load_img(
#         img_path, target_size=(CLASSIFICATION_IMG_HEIGHT, CLASSIFICATION_IMG_WIDTH)
#     )
#
#     img_array = tf.keras.utils.img_to_array(img)
#     img_array = tf.expand_dims(img_array, 0)
#
#     return img_array
#
#
# def predict_identification(img_array):
#     predictions = identification_model.predict(img_array, verbose=False)
#     score = tf.nn.softmax(predictions[0])
#
#     _type = FRUIT_TYPE_CLASS_NAMES[np.argmax(score)]
#     confidence = 100 * np.max(score)
#
#     return _type, confidence
#
#
# def predict_stages(img_array):
#     predictions = stages_model.predict(img_array, verbose=False)
#     score = tf.nn.softmax(predictions[0])
#
#     stage = FRUIT_STAGES_CLASS_NAMES[np.argmax(score)]
#     confidence = 100 * np.max(score)
#
#     return stage, confidence
