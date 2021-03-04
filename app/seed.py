import sys
import os
import asyncio

sys.path = ["", ".."] + sys.path[1:]

import sqlalchemy
from faker import Faker
from databases import Database
from dotenv import load_dotenv

from app.models.recipe import RecipeModel
from app.db.repositories.recipe_repository import RecipeRepository


async def main():
    load_dotenv()

    fake = Faker()
    metadata = sqlalchemy.MetaData()
    db_url = "{driver}://{user}:{password}@{host}:{port}/{name}".format(
        driver=os.environ.get("DB_DRIVER"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT"),
        name=os.environ.get("DB_NAME"),
    )
    database = Database(db_url)
    engine = sqlalchemy.create_engine(db_url)
    metadata.create_all(engine)

    await database.connect()

    recipe_repo = RecipeRepository(database)

    print("Seeding database...")

    for _ in range(0, 1000):
        recipe = RecipeModel(name=fake.name(), description=fake.text())
        await recipe_repo.create_recipe(recipe)

    print("Database seeded")


if __name__ == "__main__":
    asyncio.run(main())