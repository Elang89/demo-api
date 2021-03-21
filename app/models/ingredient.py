from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from sqlalchemy import Column  # type: ignore
from sqlalchemy import DateTime, String, Table, Text
from sqlalchemy.ext.declarative import declarative_base  # type: ignore

from app.models.custom import GUID  # type: ignore
from app.resources.ingredient_constants import (
    INGREDIENT_DESCRIPTION_MAX,
    INGREDIENT_NAME_MAX,
)

Base = declarative_base()


class IngredientOrm(Base):  # type: ignore
    __tablename__ = "ingredients"

    id = Column(GUID, primary_key=True)
    name = Column(String(INGREDIENT_NAME_MAX), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)

    @classmethod
    def table(cls) -> Table:
        return cls.__table__


class IngredientModel(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(max_length=INGREDIENT_NAME_MAX)
    description: str = Field(max_length=INGREDIENT_DESCRIPTION_MAX)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)

    class Config:
        orm_mode = True


class UpdatedIngredientModel(BaseModel):
    name: Optional[str] = Field(max_length=INGREDIENT_NAME_MAX)
    description: Optional[str] = Field(max_length=INGREDIENT_DESCRIPTION_MAX)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class IngredientForRecipe(BaseModel):
    id: UUID
    name: str


class UpdatedIngredientForRecipe(IngredientForRecipe):
    is_deleted: bool = Field(default=False)
