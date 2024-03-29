from typing import List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from fastapi.responses import JSONResponse

from app.api.dependencies.database import get_repository
from app.db.repositories.recipe_repository import RecipeRepository
from app.models.recipe import (
    RecipeModel,
    RecipeModelWithIngredients,
    UpdatedRecipeModel,
)
from app.resources.common_constants import (
    QUERY_DEFAULT_LIMIT,
    QUERY_DEFAULT_OFFSET,
    QUERY_MAX_LIMIT,
    STATUS_CREATED,
    STATUS_NOT_FOUND,
)
from app.resources.recipe_constants import (
    ALIAS_RECIPE,
    QUERY_RECIPE_FILTER_REGEX,
    QUERY_RECIPE_SORT_REGEX,
    RECIPE_DOES_NOT_EXIST,
    TAG_RECIPES,
)

router = APIRouter()


@router.get(
    "/{id}",
    name="recipes:get-one-recipe",
    tags=[TAG_RECIPES],
    response_class=JSONResponse,
    response_model=RecipeModelWithIngredients,
)
async def get_one_recipe(
    id: str,
    recipe_repo: RecipeRepository = Depends(get_repository(RecipeRepository)),
) -> RecipeModelWithIngredients:

    recipe = await recipe_repo.get_one_recipe(id)

    if recipe is None:
        raise HTTPException(status_code=STATUS_NOT_FOUND, detail=RECIPE_DOES_NOT_EXIST)

    return recipe


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
        regex=QUERY_RECIPE_SORT_REGEX,
    ),
    filters: Optional[List[str]] = Query(
        None,
        alias="filters",
        description="Filters for collection",
        regex=QUERY_RECIPE_FILTER_REGEX,
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
    status_code=STATUS_CREATED,
)
async def create_recipe(
    recipe: RecipeModelWithIngredients = Body(..., alias=ALIAS_RECIPE),
    recipe_repo: RecipeRepository = Depends(get_repository(RecipeRepository)),
) -> RecipeModelWithIngredients:

    return await recipe_repo.create_recipe(recipe)


@router.patch(
    "/{id}",
    name="recipes:update-recipe",
    tags=[TAG_RECIPES],
    response_class=JSONResponse,
    response_model=RecipeModelWithIngredients,
)
async def update_recipe(
    id: str,
    updated_recipe: UpdatedRecipeModel = Body(..., alias=ALIAS_RECIPE),
    recipe_repo: RecipeRepository = Depends(get_repository(RecipeRepository)),
) -> RecipeModelWithIngredients:
    recipe = await recipe_repo.update_recipe(id, updated_recipe)

    if recipe is None:
        raise HTTPException(STATUS_NOT_FOUND, detail=RECIPE_DOES_NOT_EXIST)

    return recipe


@router.delete(
    "/{id}",
    name="recipes:delete-recipe",
    tags=[TAG_RECIPES],
    response_class=JSONResponse,
    response_model=RecipeModel,
)
async def delete_recipe(
    id: str,
    recipe_repo: RecipeRepository = Depends(get_repository(RecipeRepository)),
) -> RecipeModelWithIngredients:
    recipe = await recipe_repo.delete_recipe(id)

    if recipe is None:
        raise HTTPException(STATUS_NOT_FOUND, detail=RECIPE_DOES_NOT_EXIST)

    return recipe
