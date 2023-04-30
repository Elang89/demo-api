# flake8: noqa
# type: ignore

import asyncio
import os
import random
import sys
import uuid

import sqlalchemy
from databases import Database
from dotenv import load_dotenv

from app.db.repositories.ingredient_repository import IngredientRepository
from app.db.repositories.recipe_repository import RecipeRepository
from app.models.ingredient import IngredientModel
from app.models.recipe import RecipeModelWithIngredients

sys.path = ["", ".."] + sys.path[1:]


async def main() -> None:
    load_dotenv()

    metadata = sqlalchemy.MetaData()
    db_url = "postgres://{user}:{password}@{host}:{port}/{name}".format(
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT"),
        name=os.environ.get("DB_NAME"),
    )
    database = Database(db_url)
    engine = sqlalchemy.create_engine(db_url)
    metadata.create_all(engine)
    ingredient_list = []

    await database.connect()

    recipe_repo = RecipeRepository(database)
    ingredient_repo = IngredientRepository(database)

    print("Seeding database...")

    for _ in range(0, 1000):
        ingredient = IngredientModel(name=str(uuid.uuid4()), description=fake.text())
        ingredient_list.append(ingredient)
        await ingredient_repo.create_ingredient(ingredient)

    for _ in range(0, 1000):
        ingredients = random.sample(ingredient_list, 5)
        recipe = RecipeModelWithIngredients(
            name=str(uuid.uuid4()), description=fake.text(), ingredients=ingredients
        )
        await recipe_repo.create_recipe(recipe)

    print("Database seeded")


if __name__ == "__main__":
    asyncio.run(main())
