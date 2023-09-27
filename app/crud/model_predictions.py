import io
import numpy as np
import tensorflow as tf

from app.core.config import settings

type_class_model = tf.keras.models.load_model(settings.TYPE_CLASSIFICATION_MODEL_PATH)
maturation_stage_class_model = tf.keras.models.load_model(
    settings.STAGE_MATURATION_CLASSIFICATION_MODEL_PATH
)

FRUIT_STAGES_CLASS_NAMES = ["RAW", "UNRIPE", "RIPE", "OVERRIPE", "ROTTEN"]
FRUIT_TYPE_CLASS_NAMES = ["APPLE", "BANANA", "ORANGE"]


def predict(img_file):
    img = tf.keras.utils.load_img(
        io.BytesIO(img_file.file.read()),
        target_size=(
            settings.CLASSIFICATION_IMG_HEIGHT,
            settings.CLASSIFICATION_IMG_WIDTH,
        ),
    )

    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)

    fruit_type_class, fruit_type_confidence = predict_identification(img_array)
    fruit_stage_class, fruit_stage_confidence = None, None

    if fruit_type_class == "BANANA":
        fruit_stage_class, fruit_stage_confidence = predict_stages(img_array)

    return {
        "type": {"name": fruit_type_class, "confidence": fruit_type_confidence},
        "maturation_stage": {
            "name": fruit_stage_class,
            "confidence": fruit_stage_confidence,
        },
    }


def __image_to_image_array(img_path):
    img = tf.keras.utils.load_img(
        img_path,
        target_size=(
            settings.CLASSIFICATION_IMG_HEIGHT,
            settings.CLASSIFICATION_IMG_WIDTH,
        ),
    )

    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)

    return img_array


def predict_identification(img_array):
    predictions = type_class_model.predict(img_array, verbose=False)
    score = tf.nn.softmax(predictions[0])

    _type = FRUIT_TYPE_CLASS_NAMES[np.argmax(score)]
    confidence = 100 * np.max(score)

    return _type, confidence


def predict_stages(img_array):
    predictions = maturation_stage_class_model.predict(img_array, verbose=False)
    score = tf.nn.softmax(predictions[0])

    stage = FRUIT_STAGES_CLASS_NAMES[np.argmax(score)]
    confidence = 100 * np.max(score)

    return stage, confidence
