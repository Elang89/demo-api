from fastapi import APIRouter

from app.api.routes import ingredients, recipes
from app.resources.constants import TAG_INGREDIENTS, TAG_RECIPES

router = APIRouter()
router.include_router(recipes.router, tags=[TAG_RECIPES], prefix="/recipes")
router.include_router(ingredients.router, tags=[TAG_INGREDIENTS], prefix="/ingredients")
