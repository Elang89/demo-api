import random
import uuid
from typing import List

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from mimesis.random import Random
from starlette import status

from app.models.ingredient import IngredientModel
from app.models.recipe import (
    RecipeModel,
    RecipeModelWithIngredients,
    UpdatedRecipeModel,
)
from tests.common.constants import RECIPE_DESCRIPTION_LENGTH, RECIPE_NAME_LENGTH

pytestmark = pytest.mark.asyncio


GET_RECIPES_ROUTE = "recipes:get-recipes"
GET_ONE_RECIPES_ROUTE = "recipes:get-one-recipe"
POST_RECIPES_ROUTE = "recipes:create-recipe"
UPDATE_RECIPES_ROUTE = "recipes:update-recipe"
DELETE_RECIPES_ROUTE = "recipes:delete-recipe"


async def test_create_recipe(
    app: FastAPI,
    client: AsyncClient,
    random_generator: Random,
    test_multiple_ingredients: List[IngredientModel],
) -> None:
    new_recipe = RecipeModel(
        name=random_generator.randstr(length=RECIPE_NAME_LENGTH),
        description=random_generator.randstr(length=RECIPE_DESCRIPTION_LENGTH),
    )

    ingredients = [
        ingredient.dict() for ingredient in random.sample(test_multiple_ingredients, 5)
    ]

    ingredients = [
        {"id": str(ingredient.get("id")), "name": ingredient.get("name")}
        for ingredient in ingredients
    ]

    response = await client.post(
        app.url_path_for(POST_RECIPES_ROUTE),
        json={
            "id": str(new_recipe.id),
            "name": new_recipe.name,
            "description": new_recipe.description,
            "ingredients": ingredients,
        },
    )

    assert response.status_code == status.HTTP_201_CREATED

    recipe = RecipeModel(**response.json())

    assert str(recipe.id) == str(new_recipe.id)
    assert recipe.name == new_recipe.name
    assert recipe.description == new_recipe.description


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
        app.url_path_for(GET_RECIPES_ROUTE), params={"filters": r"name LIKE '%s%'"}
    )

    assert response.status_code == status.HTTP_200_OK

    recipes = [RecipeModel(**recipe) for recipe in response.json()]

    assert recipes == list(
        filter(lambda recipe: "s" in recipe.name, recipes),
    )


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
        params={"sort": ["name:asc", "created_at:desc"], "filters": r"name LIKE '%s%'"},
    )

    assert response.status_code == status.HTTP_200_OK

    recipes = [RecipeModel(**recipe) for recipe in response.json()]

    assert recipes == sorted(recipes, key=lambda recipe: recipe.name)
    assert recipes == list(filter(lambda recipe: "s" in recipe.name, recipes))


async def test_get_one_recipe(
    app: FastAPI, client: AsyncClient, test_recipe: RecipeModel
) -> None:
    recipe_id = test_recipe.id

    response = await client.get(app.url_path_for(GET_ONE_RECIPES_ROUTE, id=recipe_id))

    assert response.status_code == status.HTTP_200_OK
    recipe = RecipeModel(**response.json())

    assert recipe.id == test_recipe.id
    assert recipe.name == test_recipe.name
    assert recipe.description == test_recipe.description


async def test_get_one_not_found_recipe(app: FastAPI, client: AsyncClient) -> None:
    recipe_id = str(uuid.uuid4())

    response = await client.get(app.url_path_for(GET_ONE_RECIPES_ROUTE, id=recipe_id))

    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_update_recipe(
    app: FastAPI,
    client: AsyncClient,
    test_recipe: RecipeModelWithIngredients,
    test_ingredient: IngredientModel,
) -> None:

    ingredients = [
        {"id": str(ingredient.id), "name": ingredient.name, "is_deleted": True}
        for ingredient in test_recipe.ingredients
    ]

    ingredients.append({"id": str(test_ingredient.id), "name": test_ingredient.name})

    recipe = UpdatedRecipeModel(
        name="Something Else", description="Some other thing", ingredients=ingredients
    )

    response = await client.patch(
        app.url_path_for(UPDATE_RECIPES_ROUTE, id=test_recipe.id),
        json={
            "name": recipe.name,
            "description": recipe.description,
            "ingredients": ingredients,
        },
    )

    assert response.status_code == status.HTTP_200_OK

    updated_recipe = RecipeModelWithIngredients(**response.json())

    assert test_recipe.id == updated_recipe.id
    assert recipe.name == updated_recipe.name
    assert recipe.description == updated_recipe.description
    assert len(recipe.ingredients) != len(updated_recipe.ingredients)


async def test_update_not_found_recipe(app: FastAPI, client: AsyncClient) -> None:
    recipe_id = str(uuid.uuid4())

    response = await client.patch(
        app.url_path_for(UPDATE_RECIPES_ROUTE, id=recipe_id),
        json={"name": "Something", "description": "something else"},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_delete_recipe(
    app: FastAPI, client: AsyncClient, test_recipe: RecipeModel
) -> None:
    response = await client.delete(
        app.url_path_for(DELETE_RECIPES_ROUTE, id=test_recipe.id)
    )

    assert response.status_code == status.HTTP_200_OK

    deleted_recipe = RecipeModel(**response.json())

    assert deleted_recipe.id == test_recipe.id


async def test_delete_not_found_recipe(app: FastAPI, client: AsyncClient) -> None:
    recipe_id = str(uuid.uuid4())

    response = await client.get(app.url_path_for(GET_ONE_RECIPES_ROUTE, id=recipe_id))

    assert response.status_code == status.HTTP_404_NOT_FOUND
