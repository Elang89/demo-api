from typing import List, Optional

from fastapi import APIRouter, Body, Depends, Query, HTTPException
from fastapi.responses import JSONResponse

from app.resources.constants import (
    TAG_INGREDIENTS,
    ALIAS_INGREDIENT,
    QUERY_DEFAULT_LIMIT,
    QUERY_DEFAULT_OFFSET,
)
from app.models.ingredient import IngredientModel

router = APIRouter()


@router.get(
    "{id}",
    name="ingredients:get-one-ingredient",
    tags=[TAG_INGREDIENTS],
    response_class=JSONResponse,
    response_model=IngredientModel,
)
async def get_one_ingredient(id: str) -> IngredientModel:
    raise NotImplementedError()


@router.get(
    "",
    name="ingredients:get-ingredients",
    tags=[TAG_INGREDIENTS],
    response_class=JSONResponse,
    response_model=List[IngredientModel],
)
async def get_ingredients(
    limit: int = Query(
        QUERY_DEFAULT_LIMIT, alias="limit", description="Ingredients per page"
    ),
    offset: int = Query(
        QUERY_DEFAULT_OFFSET, alias="offset", description="Pagination offset"
    ),
    sort: Optional[List[str]] = Query(
        None, alias="sort", description="Sorting for collection"
    ),
    filters: Optional[List[str]] = Query(
        None, alias="filters", description="Filters for collection"
    ),
) -> List[IngredientModel]:
    raise NotImplementedError()


@router.post(
    "",
    name="ingredients:create-ingredient",
    tags=[TAG_INGREDIENTS],
    response_class=JSONResponse,
    response_model=IngredientModel,
)
async def create_ingredient(
    ingredient: IngredientModel = Body(..., alias=ALIAS_INGREDIENT)
) -> IngredientModel:
    raise NotImplementedError()


@router.patch(
    "/{id}",
    name="ingredients:update-ingredient",
    tags=[TAG_INGREDIENTS],
    response_class=JSONResponse,
    response_model=IngredientModel,
)
async def update_ingredient(
    id: str,
    updated_ingredient=Body(..., alias=ALIAS_INGREDIENT),
) -> IngredientModel:
    raise NotImplementedError()


@router.delete(
    "/{id}",
    name="ingredients:delete-ingredient",
    tags=[TAG_INGREDIENTS],
    response_class=JSONResponse,
    response_model=IngredientModel,
)
async def delete_ingredient(id: str) -> IngredientModel:
    raise NotImplementedError()