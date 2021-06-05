from sqlalchemy import Column  # type: ignore
from sqlalchemy import ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore

Base = declarative_base()

recipes_ingredients = Table(
    "recipes_ingredients",
    Base.metadata,
    Column("recipe_id", UUID, ForeignKey("recipes.id"), primary_key=True),
    Column("ingredient_id", UUID, ForeignKey("ingredients.id"), primary_key=True),
)
