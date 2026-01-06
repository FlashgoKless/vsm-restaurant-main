from sqlalchemy import Column
from sqlalchemy.dialects.sqlite import INTEGER, VARCHAR
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import SQLModel, Field


class MenuItem(SQLModel, table=True):
    """Menu item.

    composition is a JSON array like:
      [{"ingredient_id": 1, "quantity": 2}, ...]
    """

    __tablename__ = "menu"

    id: int | None = Field(primary_key=True, default=None)
    name: str = Field(sa_column=Column(VARCHAR(255)))
    price: int = Field(sa_column=Column(INTEGER))
    composition: list[dict] | None = Field(sa_column=Column(JSONB), default=None)
    is_available: bool = Field(default=True)
