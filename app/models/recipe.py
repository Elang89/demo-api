from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from app.models.custom import GUID
from app.models.ingredient import IngredientForRecipe, UpdatedIngredientForRecipe
from app.models.recipes_ingredients import recipes_ingredients

Base = declarative_base()


class RecipeOrm(Base):
    __tablename__ = "recipes"

    id = Column(GUID, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)
    children = relationship(
        "Ingredient", secondary=recipes_ingredients, order_by="Ingredient.name"
    )

    @classmethod
    def table(cls):
        return cls.__table__


class RecipeModel(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(max_length=50)
    description: str = Field(max_length=500)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)

    class Config:
        orm_mode = True


class RecipeModelWithIngredients(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(max_length=50)
    description: str = Field(max_length=500)
    ingredients: List[IngredientForRecipe]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)


class UpdatedRecipeModel(BaseModel):
    name: Optional[str] = Field(max_length=50)
    description: Optional[str] = Field(max_length=500)
    ingredients: Optional[List[UpdatedIngredientForRecipe]]
    updated_at: datetime = Field(default_factory=datetime.utcnow)
