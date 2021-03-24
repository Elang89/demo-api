import logging
import sys

from loguru import logger
from starlette.config import Config

from app.core.logging import InterceptHandler

# Api Prefix
API_PREFIX = "/api/v1"

# Api Version
VERSION = "0.1.0"

# Env variable config
config = Config(".env")

DEBUG: bool = config("DEBUG", cast=bool, default=False)
PROJECT_NAME: str = config("PROJECT_NAME", default="Food Automator API")

# Database
DB_HOST: str = config("DB_HOST", default="0.0.0.0")
DB_PORT: str = config("DB_PORT", default="5432")
DB_NAME: str = config("DB_NAME", default="food")
DB_USER: str = config("DB_USER", default="root")
DB_PASSWORD: str = config("DB_PASSWORD", default="password")


# Log settings
LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
LOGGERS = ("uvicorn.asgi", "uvicorn.access")

logging.getLogger().handlers = [InterceptHandler()]
for logger_name in LOGGERS:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]

logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])
