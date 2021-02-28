from typing import List, Optional

from fastapi import APIRouter, Body, Depends, Query
from fastapi.responses import JSONResponse

from app.api.dependencies.database import get_repository
from app.db.repositories.recipe_repository import RecipeRepository
from app.models.recipe import RecipeModel
from app.resources.constants import (
    ALIAS_RECIPE,
    QUERY_DEFAULT_LIMIT,
    QUERY_DEFAULT_OFFSET,
    QUERY_MAX_LIMIT,
    POST_RECIPE_STATUS,
    TAG_RECIPES,
)

router = APIRouter()


@router.get(
    "/{recipe_id}",
    name="recipes:get-one-recipes",
    tags=[TAG_RECIPES],
    response_class=JSONResponse,
    response_model=RecipeModel,
)
async def get_one_recipe(
    id: str,
) -> RecipeModel:
    raise NotImplementedError()


@router.get(
    "",
    name="recipes:get-recipes",
    tags=[TAG_RECIPES],
    response_class=JSONResponse,
    response_model=List[RecipeModel],
)
async def get_recipes(
    limit: int = Query(
        QUERY_DEFAULT_LIMIT,
        le=QUERY_MAX_LIMIT,
        alias="limit",
        description="Recipes per page",
    ),
    offset: int = Query(
        QUERY_DEFAULT_OFFSET,
        alias="offset",
        description="Pagination offset",
    ),
    sort: Optional[List[str]] = Query(
        None,
        alias="sort",
        description="Sorting for collection",
    ),
    filters: Optional[List[str]] = Query(
        None,
        alias="filters",
        description="Filters for collection",
    ),
    recipe_repo: RecipeRepository = Depends(get_repository(RecipeRepository)),
) -> List[RecipeModel]:
    sort_params = {}

    if sort:
        param_list = [sort_param.split(":") for sort_param in sort]
        sort_params = {sort_param[0]: sort_param[1] for sort_param in param_list}

    return await recipe_repo.get_recipes(
        limit,
        offset,
        sort_params=sort_params,
        filters=filters,
    )


@router.post(
    "",
    name="recipes:create-recipe",
    tags=[TAG_RECIPES],
    response_model=RecipeModel,
    response_class=JSONResponse,
    status_code=POST_RECIPE_STATUS,
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
    response_class=JSONResponse,
    response_model=RecipeModel,
)
async def update_recipe(id: str) -> RecipeModel:
    raise NotImplementedError()


@router.delete(
    "/{recipe_id}",
    name="recipes:delete-recipe",
    tags=[TAG_RECIPES],
    response_class=JSONResponse,
    response_model=RecipeModel,
)
async def delete_recipe(
    id: str,
) -> RecipeModel:
    raise NotImplementedError()
