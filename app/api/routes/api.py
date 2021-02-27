from fastapi import APIRouter

from app.api.routes import recipes

router = APIRouter()
router.include_router(recipes.router, tags=["recipes"], prefix="/recipes")
