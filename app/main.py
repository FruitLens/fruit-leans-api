import io
import os

import numpy as np
import tensorflow as tf
from fastapi import FastAPI, UploadFile

IMG_HEIGHT = 180
IMG_WIDTH = 180
FRUIT_TYPE_CLASS_NAMES = ["APPLE", "BANANA", "ORANGE"]

app = FastAPI()

# outside docker
# model = tf.keras.models.load_model(os.path.join("../models", "fruitclassifier.h5"))

# inside docker
model = tf.keras.models.load_model(os.path.join("./fruitclassifier.h5"))


@app.get("/")
async def root():
    return "FruitLens API"


@app.post("/predict/fruit-type")
async def predict_fruit_type_from_image(file: UploadFile):
    img = io.BytesIO(file.file.read())

    fruit_type_class, confidence = __predict_image_from_path(img)

    return {"predicted_class": fruit_type_class, "confidence": confidence}


def __predict_image_from_path(img_path):
    img = tf.keras.utils.load_img(img_path, target_size=(IMG_HEIGHT, IMG_WIDTH))

    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)

    predictions = model.predict(img_array, verbose=False)
    score = tf.nn.softmax(predictions[0])

    fruit_type_class = FRUIT_TYPE_CLASS_NAMES[np.argmax(score)]
    confidence = 100 * np.max(score)
    # print(
    #     "This image most likely belongs to {} with a {:.2f} percent confidence.".format(
    #         fruit_type_class, confidence
    #     )
    # )

    return fruit_type_class, confidence
