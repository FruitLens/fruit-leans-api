import io
import os

import numpy as np
import tensorflow as tf
from fastapi import FastAPI, UploadFile

IMG_HEIGHT = 256
IMG_WIDTH = 256
FRUIT_TYPE_CLASS_NAMES = ["APPLE", "BANANA", "ORANGE"]
FRUIT_STAGES_CLASS_NAMES = ["OVERRIPE", "RAW", "RIPE"]

app = FastAPI()

# outside docker
identification_model = tf.keras.models.load_model(
    os.path.join("../models", "fruit_type_classifier_v2.h5")
)
stages_model = tf.keras.models.load_model(
    os.path.join("../models", "banana_stages_classifier_v3.h5")
)


# inside docker
# identification_model = tf.keras.models.load_model(os.path.join("./fruit_type_classifier_v2.h5"))
# banana_stages_model = tf.keras.models.load_model(os.path.join("./banana_stages_classifier_v3.h5"))


@app.get("/")
async def root():
    return "FruitLens API"


@app.post("/predict/fruit")
async def predict_fruit_from_image(file: UploadFile):
    img = io.BytesIO(file.file.read())

    img_array = __image_to_image_array(img)

    fruit_type_class, fruit_type_confidence = predict_identification(img_array)
    fruit_stage_class, fruit_stage_confidence = None, None

    if fruit_type_class == "BANANA":
        fruit_stage_class, fruit_stage_confidence = predict_stages(img_array)

    return {
        "type": {"name": fruit_type_class, "confidence": fruit_type_confidence},
        "stage": {"name": fruit_stage_class, "confidence": fruit_stage_confidence},
    }


def __image_to_image_array(img_path):
    img = tf.keras.utils.load_img(img_path, target_size=(IMG_HEIGHT, IMG_WIDTH))

    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)

    return img_array


def predict_identification(img_array):
    predictions = identification_model.predict(img_array, verbose=False)
    score = tf.nn.softmax(predictions[0])

    _type = FRUIT_TYPE_CLASS_NAMES[np.argmax(score)]
    confidence = 100 * np.max(score)

    return _type, confidence


def predict_stages(img_array):
    predictions = stages_model.predict(img_array, verbose=False)
    score = tf.nn.softmax(predictions[0])

    stage = FRUIT_STAGES_CLASS_NAMES[np.argmax(score)]
    confidence = 100 * np.max(score)

    return stage, confidence
