from fastapi import APIRouter

from app.api.api_v1.endpoints import analyses, fruit_types, fruit_maturation_stages

api_router = APIRouter()
api_router.include_router(analyses.router)
api_router.include_router(fruit_types.router)
api_router.include_router(fruit_maturation_stages.router)
