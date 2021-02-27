from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import Column, String, Text, DateTime
from pydantic import BaseModel, Field
from sqlalchemy.ext.declarative import declarative_base

from app.models.custom import GUID


Base = declarative_base()


class RecipeOrm(Base):
    __tablename__ = "recipes"

    id = Column(GUID, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)

    @classmethod
    def table(cls):
        return cls.__table__


class RecipeModel(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(max_length=50)
    description: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True