import secrets
import os
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, HttpUrl, PostgresDsn, validator


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    # SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    # ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # SERVER_NAME: str
    # SERVER_HOST: AnyHttpUrl
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # @validator("BACKEND_CORS_ORIGINS", pre=True)
    # def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
    #     if isinstance(v, str) and not v.startswith("["):
    #         return [i.strip() for i in v.split(",")]
    #     elif isinstance(v, (list, str)):
    #         return v
    #     raise ValueError(v)

    PROJECT_NAME: str

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    CLASSIFICATION_IMG_HEIGHT: int = 256
    CLASSIFICATION_IMG_WIDTH: int = 256
    # FRUIT_TYPE_CLASS_NAMES = ["APPLE", "BANANA", "ORANGE"]
    # FRUIT_STAGES_CLASS_NAMES = ["OVERRIPE", "RAW", "RIPE"]
    S3_BUCKET_NAME: str = "fruit-lens-dream-team-training-data"

    TYPE_CLASSIFICATION_MODEL_NAME: str = "fruits_model_v2.hdf5"
    STAGE_MATURATION_CLASSIFICATION_MODEL_NAME: str = "bananas_model_v2.hdf5"

    TYPE_CLASSIFICATION_MODEL_PATH: str = os.path.join(
        "models", TYPE_CLASSIFICATION_MODEL_NAME
    )
    STAGE_MATURATION_CLASSIFICATION_MODEL_PATH: str = os.path.join(
        "models", STAGE_MATURATION_CLASSIFICATION_MODEL_NAME
    )

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
