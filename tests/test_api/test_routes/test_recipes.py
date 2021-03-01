from typing import List

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status

from app.models.recipe import RecipeModel, UpdatedRecipeModel

pytestmark = pytest.mark.asyncio


GET_RECIPES_ROUTE = "recipes:get-recipes"
GET_ONE_RECIPES_ROUTE = "recipes:get-one-recipe"
POST_RECIPES_ROUTE = "recipes:create-recipe"
UPDATE_RECIPES_ROUTE = "recipes:update-recipe"
DELTE_RECIPES_ROUTE = "recipes:delete-recipe"


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
        app.url_path_for(POST_RECIPES_ROUTE),
        json={"id": id, "name": name, "description": description},
    )

    assert response.status_code == status.HTTP_201_CREATED

    recipe = RecipeModel(**response.json())

    assert str(recipe.id) == id
    assert recipe.name == name
    assert recipe.description == description


async def test_create_unprocessable_recipe(app: FastAPI, client: AsyncClient) -> None:
    response = await client.post(
        app.url_path_for(POST_RECIPES_ROUTE), json={"stuff": "something"}
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_get_recipes(app: FastAPI, client: AsyncClient) -> None:
    response = await client.get(app.url_path_for(GET_RECIPES_ROUTE))

    assert response.status_code == status.HTTP_200_OK

    recipes = response.json()

    assert isinstance(recipes, list) == True
    assert len(recipes) <= 200


async def test_get_sorted_recipes(
    app: FastAPI, client: AsyncClient, test_multiple_recipes: List[RecipeModel]
) -> None:
    response = await client.get(
        app.url_path_for(GET_RECIPES_ROUTE),
        params={"sort": "name:asc"},
    )

    assert response.status_code == status.HTTP_200_OK

    recipes = [RecipeModel(**recipe) for recipe in response.json()]

    assert recipes == sorted(recipes, key=lambda recipe: recipe.name)


async def test_get_filtered_recipes(
    app: FastAPI, client: AsyncClient, test_multiple_recipes: List[RecipeModel]
) -> None:
    response = await client.get(
        app.url_path_for(GET_RECIPES_ROUTE), params={"filters": r"name LIKE 's%'"}
    )

    assert response.status_code == status.HTTP_200_OK

    recipes = [RecipeModel(**recipe) for recipe in response.json()]

    assert recipes == list(filter(lambda recipe: recipe.name.contains("s"), recipes))


async def test_get_unprocessable_sorted_recipes(
    app: FastAPI, client: AsyncClient
) -> None:
    response = await client.get(
        app.url_path_for(GET_RECIPES_ROUTE), params={"sort": "someword:up"}
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_get_unprocessable_filtered_recipes(
    app: FastAPI, client: AsyncClient
) -> None:
    response = await client.get(
        app.url_path_for(GET_RECIPES_ROUTE), params={"filters": "; DROP TABLE recipes"}
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_get_filtered_and_sorted_recipes(
    app: FastAPI, client: AsyncClient, test_multiple_recipes: List[RecipeModel]
) -> None:
    response = await client.get(
        app.url_path_for(GET_RECIPES_ROUTE),
        params={"sort": "name:asc,created_at:desc", "filters": r"name LIKE 's%'"},
    )

    assert response.status_code == status.HTTP_200_OK

    recipes = [RecipeModel(**recipe) for recipe in response.json()]

    assert recipes == sorted(recipes, key=lambda recipe: recipe.name)
    assert recipes == list(filter(lambda recipe: recipe.name.contains("f"), recipes))


async def test_get_one_recipe(
    app: FastAPI, client: AsyncClient, test_recipe: RecipeModel
) -> None:
    recipe_id = test_recipe.id

    response = await client.get(app.url_path_for(GET_ONE_RECIPES_ROUTE, id=recipe_id))

    assert response.status_code == status.HTTP_200_OK
    recipe = RecipeModel(**response.json())

    assert recipe.id == test_recipe.id


async def test_update_recipe(
    app: FastAPI, client: AsyncClient, test_recipe: RecipeModel
) -> None:
    recipe = UpdatedRecipeModel(name="Something Else", description="Some other thing")

    response = await client.patch(
        app.url_path_for(UPDATE_RECIPES_ROUTE, id=test_recipe.id),
        json={"name": recipe.name, "description": recipe.description},
    )

    assert response.status_code == status.HTTP_200_OK

    updated_recipe = RecipeModel(**response.json())

    assert updated_recipe.id == test_recipe.id
    assert recipe.name == updated_recipe.name
    assert recipe.description == updated_recipe.description


@pytest.mark.skip(reason="Not implemented")
async def test_update_not_found_recipe(app: FastAPI, client: AsyncClient) -> None:
    pass


async def test_delete_recipe(
    app: FastAPI, client: AsyncClient, test_recipe: RecipeModel
) -> None:
    response = await client.delete(
        app.url_path_for(DELTE_RECIPES_ROUTE, id=test_recipe.id)
    )

    assert response.status_code == status.HTTP_200_OK

    deleted_recipe = RecipeModel(**response.json())

    assert deleted_recipe.id == test_recipe.id


@pytest.mark.skip(reason="Not Implemented")
async def test_delete_not_found_recipe(app: FastAPI, client: AsyncClient) -> None:
    pass
