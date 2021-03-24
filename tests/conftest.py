import time
from os import environ, getenv

import docker as libdocker
import pytest
from asgi_lifespan import LifespanManager
from databases import Database
from fastapi import FastAPI
from httpx import AsyncClient
from mimesis.random import Random

import alembic.config
from alembic.config import Config

PG_DOCKER_IMAGE = "postgres:13.0-alpine"
PG_DOCKER_CONTAINER_NAME = "test-postgres"

USE_LOCAL_DB = getenv("USE_LOCAL_DB_FOR_TEST", False)

pytest_plugins = ["tests.common.fixtures_ingredient", "tests.common.fixtures_recipe"]


@pytest.fixture
def docker() -> libdocker.APIClient:
    with libdocker.APIClient(version="auto") as client:
        yield client


@pytest.fixture(autouse=True)
def db_server(docker: libdocker.APIClient, worker_id: str) -> None:

    if USE_LOCAL_DB is not False:
        if worker_id == "master":
            Config()
            container = docker.create_container(
                image=PG_DOCKER_IMAGE,
                name=PG_DOCKER_CONTAINER_NAME,
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

            yield container

            docker.kill(container["Id"])
            docker.remove_container(container["Id"])
        else:
            yield
    yield
    return


@pytest.fixture(autouse=True)
def apply_migrations(db_server: None, worker_id: str) -> None:
    if worker_id == "master":
        alembic.config.main(argv=["upgrade", "head"])
        yield
        alembic.config.main(argv=["downgrade", "base"])
    else:
        yield


@pytest.fixture
def app(apply_migrations: None) -> FastAPI:
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
def random_generator() -> Random:
    return Random()
