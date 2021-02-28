from typing import List

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status

from app.models.recipe import RecipeModel

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "id, name, description",
    [
        ("97950e81-afb7-4146-b12b-06877de48202", "ham sandwich", "something"),
        ("7a5e2caa-d558-41bc-8703-837b16a5b6c6", "hamburger", "something"),
    ],
)
async def test_create_recipe(
    app: FastAPI, client: AsyncClient, id: str, name: str, description: str
) -> None:
    response = await client.post(
        app.url_path_for("recipes:create-recipe"),
        json={"id": id, "name": name, "description": description},
    )

    assert response.status_code == status.HTTP_201_CREATED

    recipe = RecipeModel(**response.json())

    assert str(recipe.id) == id
    assert recipe.name == name
    assert recipe.description == description


@pytest.mark.skip(reason="Not Implemented")
async def test_create_recipe_unprocessable_entity(
    app: FastAPI, client: AsyncClient
) -> None:
    pass


async def test_get_recipes(app: FastAPI, client: AsyncClient) -> None:
    response = await client.get(app.url_path_for("recipes:get-recipes"))
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(data, list) == True
    assert len(data) <= 200


async def test_get_sorted_recipes(
    app: FastAPI, client: AsyncClient, test_multiple_recipes: List[RecipeModel]
) -> None:
    response = await client.get(
        app.url_path_for("recipes:get-recipes"),
        params={"sort": "name:asc"},
    )
    data = [RecipeModel(**recipe) for recipe in response.json()]

    assert response.status_code == status.HTTP_200_OK
    assert data == sorted(data, key=lambda recipe: recipe.name)


async def test_get_filtered_recipes(
    app: FastAPI, client: AsyncClient, test_multiple_recipes: List[RecipeModel]
) -> None:
    response = await client.get(
        app.url_path_for("recipes:get-recipes"), params={"filters": r"name LIKE 's%'"}
    )

    data = [RecipeModel(**recipe) for recipe in response.json()]

    assert response.status_code == status.HTTP_200_OK
    assert data == list(filter(lambda recipe: recipe.name.contains("s"), data))


@pytest.mark.skip(reason="Not Implemented")
async def test_api_get_illegal_filtered_recipes(
    app: FastAPI, client: AsyncClient
) -> None:
    pass


async def test_get_filtered_and_sorted_recipes(
    app: FastAPI, client: AsyncClient, test_multiple_recipes: List[RecipeModel]
) -> None:
    response = await client.get(
        app.url_path_for("recipes:get-recipes"),
        params={"sort": "name:asc,created_at:desc", "filters": r"name LIKE 's%'"},
    )

    data = [RecipeModel(**recipe) for recipe in response.json()]

    assert response.status_code == status.HTTP_200_OK
    assert data == sorted(data, key=lambda recipe: recipe.name)
    assert data == list(filter(lambda recipe: recipe.name.contains("f"), data))


@pytest.mark.skip(reason="Not Implemented")
async def test_get_one_recipe(
    app: FastAPI, client: AsyncClient, test_recipe: RecipeModel
) -> None:
    pass


@pytest.mark.skip(reason="Not Implemented")
async def test_update_recipe(
    app: FastAPI, client: AsyncClient, test_recipe: RecipeModel
) -> None:
    pass


@pytest.mark.skip(reason="Not implemented")
async def test_update_recipe_not_found(app: FastAPI, client: AsyncClient) -> None:
    pass


@pytest.mark.skip(reason="Not Implemented")
async def test_delete_recipe(
    app: FastAPI, client: AsyncClient, test_recipe: RecipeModel
) -> None:
    pass


@pytest.mark.skip(reason="Not Implemented")
async def test_delete_recipe_not_found(app: FastAPI, client: AsyncClient) -> None:
    pass
