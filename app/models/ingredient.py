from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.ext.declarative import declarative_base

from app.models.custom import GUID

Base = declarative_base()


class IngredientOrm(Base):
    __tablename__ = "ingredients"

    id = Column(GUID, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)

    @classmethod
    def table(cls):
        return cls.__table__


class IngredientModel(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(max_length=50)
    description: str = Field(max_length=500)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)

    class Config:
        orm_mode = True


class UpdatedIngredientModel(BaseModel):
    name: Optional[str] = Field(max_length=50)
    description: Optional[str] = Field(max_length=500)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class IngredientForRecipe(BaseModel):
    id: UUID
    name: str


class UpdatedIngredientForRecipe(IngredientForRecipe):
    is_deleted: bool = Field(default=False)
