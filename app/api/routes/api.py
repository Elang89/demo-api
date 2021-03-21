from fastapi import APIRouter

from app.api.routes import ingredients, recipes
from app.resources.ingredient_constants import TAG_INGREDIENTS
from app.resources.recipe_constants import TAG_RECIPES

router = APIRouter()
router.include_router(recipes.router, tags=[TAG_RECIPES], prefix="/recipes")
router.include_router(ingredients.router, tags=[TAG_INGREDIENTS], prefix="/ingredients")
