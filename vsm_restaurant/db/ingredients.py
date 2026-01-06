from sqlalchemy import Column
from sqlalchemy.dialects.sqlite import INTEGER, VARCHAR
from sqlmodel import SQLModel, Field


class Ingredient(SQLModel, table=True):
    """Ingredients with current stock (остаток)."""

    __tablename__ = "ingredients"

    id: int | None = Field(primary_key=True, default=None)
    name: str = Field(sa_column=Column(VARCHAR(255)))
    stock: int = Field(sa_column=Column(INTEGER), default=0)
