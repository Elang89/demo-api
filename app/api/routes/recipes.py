from typing import List, Optional
from fastapi import APIRouter, Body, Depends, HTTPException, Query
from starlette import status

from app.models.recipe import RecipeModel
from app.resources.constants import RECIPE_DOES_NOT_EXIST
from app.api.dependencies.database import get_repository
from app.db.repositories.recipe_repository import RecipeRepository

router = APIRouter()

TAG_RECIPES = "recipes"
ALIAS_RECIPE = "recipe"


@router.get(
    "/{recipe_id}",
    name="recipes:get-one",
    tags=[TAG_RECIPES],
    response_model=RecipeModel,
)
async def get_recipe(
    id: str,
) -> RecipeModel:
    pass


@router.get(
    "",
    name="recipes:get-recipes",
    tags=[TAG_RECIPES],
    response_model=List[RecipeModel],
)
async def get_recipes(
    limit: int = Query(50, le=200, alias="limit", description="Recipes per page"),
    offset: int = Query(0, alias="offset", description="Pagination offset"),
    sort: Optional[List[str]] = Query(None),
    recipe_repo: RecipeRepository = Depends(get_repository(RecipeRepository)),
) -> List[RecipeModel]:
    sort_params = {}
    filters = {}

    if sort:
        sort_params = {
            sort_param[0]: sort_param[1]
            for sort_param in [param.split(":") for param in sort]
        }

    return await recipe_repo.get_recipes(
        limit, offset, sort_params=sort_params, filters=filters
    )


@router.post(
    "", name="recipes:create-recipe", tags=[TAG_RECIPES], response_model=RecipeModel
)
async def create_recipe(
    recipe: RecipeModel = Body(..., alias=ALIAS_RECIPE),
    recipe_repo: RecipeRepository = Depends(get_repository(RecipeRepository)),
) -> RecipeModel:
    return await recipe_repo.create_recipe(recipe)


@router.patch(
    "/{recipe_id}",
    name="recipes:update-recipe",
    tags=[TAG_RECIPES],
    response_model=RecipeModel,
)
async def update_recipe(id: str) -> RecipeModel:
    pass


@router.delete(
    "/{recipe_id}",
    name="recipes:delete-recipe",
    tags=[TAG_RECIPES],
    response_model=RecipeModel,
)
async def delete_recipe(
    id: str,
) -> RecipeModel:
    pass
