import uuid
from typing import List

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from mimesis.random import Random
from starlette import status

from app.models.ingredient import IngredientModel, UpdatedIngredientModel
from tests.common.constants import INGREDIENT_DESCRIPTION_LENGTH, INGREDIENT_NAME_LENGTH

pytestmark = pytest.mark.asyncio

GET_INGREDIENTS_ROUTE = "ingredients:get-ingredients"
GET_ONE_INGREDIENTS_ROUTE = "ingredients:get-one-ingredient"
POST_INGREDIENTS_ROUTE = "ingredients:create-ingredient"
UPDATE_INGREDIENTS_ROUTE = "ingredients:update-ingredient"
DELETE_INGREDIENTS_ROUTE = "ingredients:delete-ingredient"


async def test_create_ingredient(
    app: FastAPI, client: AsyncClient, random_generator: Random
) -> None:
    new_ingredient = IngredientModel(
        name=random_generator.randstr(length=INGREDIENT_NAME_LENGTH),
        description=random_generator.randstr(length=INGREDIENT_DESCRIPTION_LENGTH),
    )

    response = await client.post(
        app.url_path_for(POST_INGREDIENTS_ROUTE),
        json={
            "id": str(new_ingredient.id),
            "name": new_ingredient.name,
            "description": new_ingredient.description,
        },
    )

    assert response.status_code == status.HTTP_201_CREATED

    ingredient = IngredientModel(**response.json())

    assert str(ingredient.id) == str(new_ingredient.id)
    assert ingredient.name == new_ingredient.name
    assert ingredient.description == new_ingredient.description


async def test_get_ingredient(app: FastAPI, client: AsyncClient) -> None:
    response = await client.get(app.url_path_for(GET_INGREDIENTS_ROUTE))

    assert response.status_code == status.HTTP_200_OK

    ingredients = response.json()

    assert isinstance(ingredients, list) == True
    assert len(ingredients) <= 200


async def test_get_sorted_ingredients(
    app: FastAPI, client: AsyncClient, test_multiple_ingredients: List[IngredientModel]
) -> None:
    response = await client.get(
        app.url_path_for(GET_INGREDIENTS_ROUTE), params={"sort": "created_at:asc"}
    )

    assert response.status_code == status.HTTP_200_OK

    ingredients = [IngredientModel(**ingredient) for ingredient in response.json()]

    assert ingredients == sorted(
        ingredients, key=lambda ingredient: ingredient.created_at
    )


async def test_get_filtered_ingredients(
    app: FastAPI, client: AsyncClient, test_multiple_ingredients: List[IngredientModel]
) -> None:
    response = await client.get(
        app.url_path_for(GET_INGREDIENTS_ROUTE),
        params={"filters": r"name LIKE 's%'"},
    )

    assert response.status_code == status.HTTP_200_OK

    ingredients = [IngredientModel(**ingredient) for ingredient in response.json()]

    assert ingredients == list(
        filter(lambda ingredient: "s" in ingredient.name, ingredients)
    )


async def test_get_unprocessable_sorted_ingredients(
    app: FastAPI, client: AsyncClient
) -> None:
    response = await client.get(
        app.url_path_for(GET_INGREDIENTS_ROUTE), params={"sort": "someword:up"}
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_get_unprocessable_filtered_ingredients(
    app: FastAPI, client: AsyncClient
) -> None:
    response = await client.get(
        app.url_path_for(GET_INGREDIENTS_ROUTE),
        params={"filters": "; DROP TABLE ingredients"},
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_get_filtered_and_sorted_ingredients(
    app: FastAPI, client: AsyncClient, test_multiple_ingredients: List[IngredientModel]
) -> None:
    response = await client.get(
        app.url_path_for(GET_INGREDIENTS_ROUTE),
        params={"sort": ["name:asc", "created_at:desc"], "filters": r"name LIKE 'f%'"},
    )

    assert response.status_code == status.HTTP_200_OK

    ingredients = [IngredientModel(**ingredient) for ingredient in response.json()]

    sorted_ingredients = sorted(ingredients, key=lambda ingredient: ingredient.name)

    assert ingredients == sorted_ingredients
    assert ingredients == list(
        filter(lambda ingredient: "f" in ingredient.name, ingredients)
    )


async def test_get_one_ingredient(
    app: FastAPI, client: AsyncClient, test_ingredient: IngredientModel
) -> None:
    response = await client.get(
        app.url_path_for(GET_ONE_INGREDIENTS_ROUTE, id=test_ingredient.id)
    )

    assert response.status_code == status.HTTP_200_OK

    ingredient = IngredientModel(**response.json())

    assert ingredient.id == test_ingredient.id
    assert ingredient.name == test_ingredient.name
    assert ingredient.description == test_ingredient.description


async def test_get_one_not_found_ingredient(app: FastAPI, client: AsyncClient) -> None:
    ingredient_id = str(uuid.uuid4())

    response = await client.get(
        app.url_path_for(GET_ONE_INGREDIENTS_ROUTE, id=ingredient_id)
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_update_ingredient(
    app: FastAPI,
    client: AsyncClient,
    test_ingredient: IngredientModel,
    random_generator: Random,
) -> None:
    ingredient = UpdatedIngredientModel(
        name=random_generator.randstr(length=INGREDIENT_NAME_LENGTH),
        description=random_generator.randstr(length=INGREDIENT_DESCRIPTION_LENGTH),
    )

    response = await client.patch(
        app.url_path_for(UPDATE_INGREDIENTS_ROUTE, id=test_ingredient.id),
        json={"name": ingredient.name, "description": ingredient.description},
    )


async def test_update_not_found_ingredient(app: FastAPI, client: AsyncClient) -> None:
    ingredient_id = str(uuid.uuid4())

    response = await client.patch(
        app.url_path_for(UPDATE_INGREDIENTS_ROUTE, id=ingredient_id),
        json={"name": "Something", "description": "something else"},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_delete_ingredient(
    app: FastAPI, client: AsyncClient, test_ingredient: IngredientModel
) -> None:
    response = await client.delete(
        app.url_path_for(DELETE_INGREDIENTS_ROUTE, id=test_ingredient.id)
    )

    assert response.status_code == status.HTTP_200_OK

    deleted_ingredient = IngredientModel(**response.json())

    assert deleted_ingredient.id == test_ingredient.id


async def test_delete_not_found_ingredient(app: FastAPI, client: AsyncClient) -> None:
    ingredient_id = str(uuid.uuid4())

    response = await client.delete(
        app.url_path_for(DELETE_INGREDIENTS_ROUTE, id=ingredient_id)
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
