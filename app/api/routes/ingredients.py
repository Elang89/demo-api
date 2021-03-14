from typing import List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from fastapi.responses import JSONResponse

from app.api.dependencies.database import get_repository
from app.db.repositories.ingredient_repository import IngredientRepository
from app.models.ingredient import (
    IngredientForRecipe,
    IngredientModel,
    UpdatedIngredientModel,
)
from app.resources.constants import (
    ALIAS_INGREDIENT,
    INGREDIENT_DOES_NOT_EXIST,
    QUERY_DEFAULT_LIMIT,
    QUERY_DEFAULT_OFFSET,
    QUERY_INGREDIENT_FILTER_REGEX,
    QUERY_INGREDIENT_SORT_REGEX,
    STATUS_CREATED_201,
    STATUS_NOT_FOUND_404,
    TAG_INGREDIENTS,
)

router = APIRouter()


@router.get(
    "{id}",
    name="ingredients:get-one-ingredient",
    tags=[TAG_INGREDIENTS],
    response_class=JSONResponse,
    response_model=IngredientModel,
)
async def get_one_ingredient(
    id: str,
    ingredient_repo: IngredientRepository = Depends(
        get_repository(IngredientRepository)
    ),
) -> IngredientModel:

    ingredient = await ingredient_repo.get_one_ingredient(id)

    if ingredient is None:
        raise HTTPException(
            status_code=STATUS_NOT_FOUND_404, detail=INGREDIENT_DOES_NOT_EXIST
        )

    return ingredient


@router.get(
    "",
    name="ingredients:get-ingredients",
    tags=[TAG_INGREDIENTS],
    response_class=JSONResponse,
    response_model=List[IngredientModel],
)
async def get_ingredients(
    limit: int = Query(
        QUERY_DEFAULT_LIMIT,
        alias="limit",
        description="Ingredients per page",
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
        regex=QUERY_INGREDIENT_SORT_REGEX,
    ),
    filters: Optional[List[str]] = Query(
        None,
        alias="filters",
        description="Filters for collection",
        regex=QUERY_INGREDIENT_FILTER_REGEX,
    ),
    ingredient_repo: IngredientRepository = Depends(
        get_repository(IngredientRepository)
    ),
) -> List[IngredientModel]:
    sort_params = {}

    if sort:
        param_list = [sort_param.split(":") for sort_param in sort]
        sort_params = {sort_param[0]: sort_param[1] for sort_param in param_list}

    return await ingredient_repo.get_ingredients(
        limit,
        offset,
        sort_params=sort_params,
        filters=filters,
    )


@router.get(
    "/recipes/{id}/ingredients",
    name="ingredients:get-recipe-ingredients",
    tags=[TAG_INGREDIENTS],
    response_class=JSONResponse,
    response_model=List[IngredientForRecipe],
)
async def get_ingredients_for_recipes(
    id: str,
    ingredient_repo: IngredientRepository = Depends(
        get_repository(IngredientRepository)
    ),
) -> List[IngredientForRecipe]:
    return await ingredient_repo.get_ingredients_for_recipe(id)


@router.post(
    "",
    name="ingredients:create-ingredient",
    tags=[TAG_INGREDIENTS],
    response_class=JSONResponse,
    response_model=IngredientModel,
    status_code=STATUS_CREATED_201,
)
async def create_ingredient(
    ingredient: IngredientModel = Body(..., alias=ALIAS_INGREDIENT),
    ingredient_repo: IngredientRepository = Depends(
        get_repository(IngredientRepository)
    ),
) -> IngredientModel:
    return await ingredient_repo.create_ingredient(ingredient)


@router.patch(
    "/{id}",
    name="ingredients:update-ingredient",
    tags=[TAG_INGREDIENTS],
    response_class=JSONResponse,
    response_model=IngredientModel,
)
async def update_ingredient(
    id: str,
    updated_ingredient: UpdatedIngredientModel = Body(..., alias=ALIAS_INGREDIENT),
    ingredient_repo: IngredientRepository = Depends(
        get_repository(IngredientRepository)
    ),
) -> IngredientModel:
    ingredient = await ingredient_repo.update_ingredient(id, updated_ingredient)

    if ingredient is None:
        raise HTTPException(STATUS_NOT_FOUND_404, detail=INGREDIENT_DOES_NOT_EXIST)

    return ingredient


@router.delete(
    "/{id}",
    name="ingredients:delete-ingredient",
    tags=[TAG_INGREDIENTS],
    response_class=JSONResponse,
    response_model=IngredientModel,
)
async def delete_ingredient(
    id: str,
    ingredient_repo: IngredientRepository = Depends(
        get_repository(IngredientRepository)
    ),
) -> IngredientModel:
    ingredient = await ingredient_repo.delete_ingredient(id)

    if ingredient is None:
        raise HTTPException(STATUS_NOT_FOUND_404, detail=INGREDIENT_DOES_NOT_EXIST)

    return ingredient
