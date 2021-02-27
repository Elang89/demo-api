from typing import Callable

from fastapi import FastAPI

from app.db.events import connect_to_db
from app.utils.sync import run_in_thread


def create_startup_handler(app: FastAPI) -> Callable:  # type: ignore
    async def start_app() -> None:
        await connect_to_db(app)

    return start_app
