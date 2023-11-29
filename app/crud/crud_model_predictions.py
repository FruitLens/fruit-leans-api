import io
import cv2 as cv
import numpy as np
import tensorflow as tf

from sklearn.decomposition import PCA

from app.core.config import settings

type_class_model = tf.keras.models.load_model(settings.TYPE_CLASSIFICATION_MODEL_PATH)
maturation_stage_class_model = tf.keras.models.load_model(
    settings.STAGE_MATURATION_CLASSIFICATION_MODEL_PATH
)

FRUIT_STAGES_CLASS_NAMES = ["OVERRIPE", "RAW", "RIPE", "ROTTEN", "UNRIPE"]
FRUIT_TYPE_CLASS_NAMES = ["APPLE", "BANANA", "ORANGE"]


def predict(img_file):
    img_bytes = io.BytesIO(img_file.file.read())
    img_pca = __run_pca_on_image(img_bytes)

    img = tf.keras.utils.load_img(
        img_pca,
        target_size=(
            settings.CLASSIFICATION_IMG_HEIGHT,
            settings.CLASSIFICATION_IMG_WIDTH,
        ),
    )

    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)

    fruit_type_class, fruit_type_confidence = predict_identification(img_array)
    fruit_stage_class, fruit_stage_confidence = None, None
    model_fruit_stage_name = None

    if fruit_type_class == "BANANA":
        fruit_stage_class, fruit_stage_confidence = predict_stages(img_array)
        model_fruit_stage_name = settings.STAGE_MATURATION_CLASSIFICATION_MODEL_NAME

    return {
        "type": {"name": fruit_type_class, "confidence": fruit_type_confidence},
        "maturation_stage": {
            "name": fruit_stage_class,
            "confidence": fruit_stage_confidence,
        },
        "model_fruit_type_name": settings.TYPE_CLASSIFICATION_MODEL_NAME,
        "model_stage_name": model_fruit_stage_name,
    }


def __run_pca_on_image(img):
    file_bytes = np.asarray(bytearray(img.read()), dtype=np.uint8)

    img = cv.imdecode(file_bytes, cv.IMREAD_COLOR)
    # cv.imwrite("/Users/csantana/Dev/TCC/fruitlens-api/original.jpg", img)

    img_pca = __pca(img)
    # cv.imwrite("/Users/csantana/Dev/TCC/fruitlens-api/pca.jpg", img_pca)

    _, encoded = cv.imencode(".jpg", img_pca)

    return io.BytesIO(encoded.tobytes())


def __pca(opencv_img):
    pca_components = 50

    img_resize = cv.resize(
        opencv_img,
        (settings.CLASSIFICATION_IMG_HEIGHT, settings.CLASSIFICATION_IMG_WIDTH),
    )

    (b, g, r) = cv.split(img_resize)
    r, g, b = r / 255, g / 255, b / 255

    pca_r = PCA(n_components=pca_components)
    r_reduz = pca_r.fit_transform(r)
    pca_g = PCA(n_components=pca_components)
    g_reduz = pca_g.fit_transform(g)
    pca_b = PCA(n_components=pca_components)
    b_reduz = pca_b.fit_transform(b)

    recog_r = pca_r.inverse_transform(r_reduz)
    recog_g = pca_g.inverse_transform(g_reduz)
    recog_b = pca_b.inverse_transform(b_reduz)

    return cv.merge((recog_b, recog_g, recog_r)) * 255


def predict_identification(img_array):
    predictions = type_class_model.predict(img_array, verbose=False)
    print(predictions)
    # score = tf.nn.softmax(predictions[0])

    sel_class = np.argmax(predictions[0])

    _type = FRUIT_TYPE_CLASS_NAMES[sel_class]
    confidence = 100 * predictions[0][sel_class]

    return _type, confidence


def predict_stages(img_array):
    predictions = maturation_stage_class_model.predict(img_array, verbose=False)
    print(predictions)
    # score = tf.nn.softmax(predictions[0])

    sel_class = np.argmax(predictions[0])

    stage = FRUIT_STAGES_CLASS_NAMES[sel_class]
    confidence = 100 * predictions[0][sel_class]

    return stage, confidence
