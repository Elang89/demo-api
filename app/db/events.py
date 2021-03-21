import sqlalchemy  # type: ignore
from databases import Database
from fastapi import FastAPI
from loguru import logger

from app.core.config import DB_DRIVER, DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER


async def connect_to_db(app: FastAPI) -> None:
    logger.info(
        """
        Establishing connection to database {0}
        using driver {1} with user {2} on host and port: {3}:{4}
        """,
        repr(DB_NAME),
        repr(DB_DRIVER),
        repr(DB_USER),
        repr(DB_HOST),
        repr(DB_PORT),
    )
    metadata = sqlalchemy.MetaData()
    db_url = "{driver}://{user}:{password}@{host}:{port}/{name}".format(
        driver=DB_DRIVER,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        name=DB_NAME,
    )
    database = Database(db_url)
    engine = sqlalchemy.create_engine(db_url)
    metadata.create_all(engine)

    await database.connect()

    app.state.db = database

    logger.info("Connection established")


async def close_db_connection(app: FastAPI) -> None:
    logger.info("Closing connection to database.")

    await app.state.db.disconnect()

    logger.info("Connection closed.")
