from sqlalchemy import Column  # type: ignore
from sqlalchemy import ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base  # type: ignore

from app.models.custom import GUID  # type: ignore

Base = declarative_base()

recipes_ingredients = Table(
    "recipes_ingredients",
    Base.metadata,
    Column("recipe_id", GUID, ForeignKey("recipes.id"), primary_key=True),
    Column("ingredient_id", GUID, ForeignKey("ingredients.id"), primary_key=True),
)
