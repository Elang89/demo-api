from typing import Callable

from fastapi import FastAPI

from app.db.events import close_db_connection, connect_to_db


def create_startup_handler(app: FastAPI) -> Callable:  # type: ignore
    async def start_app() -> None:
        await connect_to_db(app)

    return start_app


def create_shutdown_handler(app: FastAPI) -> Callable:  # type: ignore
    async def stop_app() -> None:
        await close_db_connection(app)

    return stop_app
