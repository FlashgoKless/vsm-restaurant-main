from datetime import datetime

from sqlalchemy import Column
from sqlalchemy.dialects.sqlite import INTEGER, VARCHAR
from sqlmodel import SQLModel, Field


class CookingTask(SQLModel, table=True):
    """Cooking tasks for kitchen."""

    __tablename__ = "cooking_tasks"

    id: int | None = Field(primary_key=True, default=None)
    order_id: int = Field(sa_column=Column(INTEGER))
    menu_id: int = Field(sa_column=Column(INTEGER))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(sa_column=Column(VARCHAR(64)), default="queued")
