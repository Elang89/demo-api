import pytest

from typing import List
from mimesis.random import Random
from databases import Database


from tests.common.constants import (
    INGREDIENT_NAME_LENGTH,
    INGREDIENT_DESCRIPTION_LENGTH,
    RECIPE_NAME_LENGTH,
    RECIPE_DESCRIPTION_LENGTH,
)
from app.db.repositories.ingredient_repository import IngredientRepository
from app.db.repositories.recipe_repository import RecipeRepository
from app.models.ingredient import IngredientForRecipe, IngredientModel
from app.models.recipe import RecipeModelWithIngredients


@pytest.fixture
async def test_recipe(
    db: Database, random_generator: Random
) -> RecipeModelWithIngredients:
    recipe_repo = RecipeRepository(db)
    ingredient_repo = IngredientRepository(db)

    ingredient = await ingredient_repo.create_ingredient(
        IngredientModel(
            name=random_generator.randstr(length=INGREDIENT_NAME_LENGTH),
            description=random_generator.randstr(length=INGREDIENT_DESCRIPTION_LENGTH),
        )
    )

    return await recipe_repo.create_recipe(
        RecipeModelWithIngredients(
            name=random_generator.randstr(length=RECIPE_NAME_LENGTH),
            description=random_generator.randstr(length=RECIPE_DESCRIPTION_LENGTH),
            ingredients=[IngredientForRecipe(id=ingredient.id, name=ingredient.name)],
        )
    )


@pytest.fixture
async def test_multiple_recipes(
    db: Database, random_generator: Random()
) -> List[RecipeModelWithIngredients]:
    repo = RecipeRepository(db)
    recipes = []

    ingredient_repo = IngredientRepository(db)

    ingredient = await ingredient_repo.create_ingredient(
        IngredientModel(
            name=random_generator.randstr(length=INGREDIENT_NAME_LENGTH),
            description=random_generator.randstr(length=INGREDIENT_DESCRIPTION_LENGTH),
        )
    )

    for _ in range(0, 500):
        recipe = await repo.create_recipe(
            RecipeModelWithIngredients(
                name=random_generator.randstr(length=RECIPE_NAME_LENGTH),
                description=random_generator.randstr(length=RECIPE_DESCRIPTION_LENGTH),
                ingredients=[
                    IngredientForRecipe(id=ingredient.id, name=ingredient.name)
                ],
            )
        )
        recipes.append(recipe)
    return recipes