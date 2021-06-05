from datetime import datetime
from typing import List, Optional
from uuid import uuid4
import uuid

from pydantic import BaseModel, Field
from sqlalchemy import Column  # type: ignore
from sqlalchemy import DateTime, String, Table, Text
from sqlalchemy.dialects import postgresql  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore

from app.models.ingredient import IngredientForRecipe, UpdatedIngredientForRecipe
from app.models.recipes_ingredients import recipes_ingredients
from app.resources.recipe_constants import RECIPE_DESCRIPTION_MAX, RECIPE_NAME_MAX

Base = declarative_base()


class RecipeOrm(Base):  # type: ignore
    __tablename__ = "recipes"

    id = Column(postgresql.UUID, primary_key=True)
    name = Column(String(RECIPE_NAME_MAX), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)
    children = relationship(
        "Ingredient",
        secondary=recipes_ingredients,
        order_by="Ingredient.name",
    )

    @classmethod
    def table(cls) -> Table:
        return cls.__table__


class RecipeModel(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid4)
    name: str = Field(max_length=RECIPE_NAME_MAX)
    description: str = Field(max_length=RECIPE_DESCRIPTION_MAX)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)

    class Config:
        orm_mode = True


class RecipeModelWithIngredients(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid4)
    name: str = Field(max_length=RECIPE_NAME_MAX)
    description: str = Field(max_length=RECIPE_DESCRIPTION_MAX)
    ingredients: List[IngredientForRecipe]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)


class UpdatedRecipeModel(BaseModel):
    name: Optional[str] = Field(max_length=RECIPE_NAME_MAX)
    description: Optional[str] = Field(max_length=RECIPE_DESCRIPTION_MAX)
    ingredients: Optional[List[UpdatedIngredientForRecipe]]
    updated_at: datetime = Field(default_factory=datetime.utcnow)
