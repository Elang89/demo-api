import time
import uuid
from os import environ
from typing import List

import docker as libdocker
import pytest
from asgi_lifespan import LifespanManager
from databases import Database
from faker import Faker
from fastapi import FastAPI
from httpx import AsyncClient

import alembic.config
from alembic.config import Config
from app.db.repositories.recipe_repository import RecipeRepository
from app.models.recipe import RecipeModel

PG_DOCKER_IMAGE = "postgres:13.0-alpine"


@pytest.fixture(scope="session")
def docker() -> libdocker.APIClient:
    with libdocker.APIClient(version="auto") as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
def db_server(docker: libdocker.APIClient) -> None:
    Config()
    container = docker.create_container(
        image=PG_DOCKER_IMAGE,
        name="test-postgres-{}".format(uuid.uuid4()),
        detach=True,
        environment={
            "POSTGRES_USER": "root",
            "POSTGRES_PASSWORD": "password",
            "POSTGRES_DB": "food",
        },
    )

    docker.start(container=container["Id"])
    inspection = docker.inspect_container(container["Id"])
    host = inspection["NetworkSettings"]["IPAddress"]

    environ["DB_DRIVER"] = "postgresql"
    environ["DB_HOST"] = host
    environ["DB_PORT"] = "5432"
    environ["DB_NAME"] = "food"
    environ["DB_USER"] = "root"
    environ["DB_PASSWORD"] = "password"

    try:
        yield container
    finally:
        docker.kill(container["Id"])
        docker.remove_container(container["Id"])


@pytest.fixture(autouse=True)
def apply_migrations(db_server: None) -> None:
    time.sleep(2.5)

    alembic.config.main(argv=["upgrade", "head"])
    yield
    alembic.config.main(argv=["downgrade", "base"])


@pytest.fixture(scope="session")
def app() -> FastAPI:
    from app.main import get_application

    return get_application()


@pytest.fixture
async def initialized_app(app: FastAPI):
    async with LifespanManager(app):
        yield app


@pytest.fixture
async def client(initialized_app: FastAPI):
    async with AsyncClient(
        app=initialized_app,
        base_url="http://testserver",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client


@pytest.fixture
def db(initialized_app: FastAPI) -> Database:
    return initialized_app.state.db


@pytest.fixture
async def test_recipe(db: Database, faker: Faker) -> RecipeModel:
    repo = RecipeRepository(db)

    return await repo.create_recipe(
        RecipeModel(name=faker.name(), description=faker.text())
    )


@pytest.fixture
async def test_multiple_recipes(db: Database, faker: Faker) -> List[RecipeModel]:
    repo = RecipeRepository(db)
    recipes = []

    for _ in range(0, 50):
        recipe = await repo.create_recipe(
            RecipeModel(name=faker.name(), description=faker.text())
        )
        recipes.append(recipe)
    return recipes
