from datetime import datetime

from sqlalchemy import Column
from sqlalchemy.dialects.sqlite import INTEGER, VARCHAR
from sqlmodel import SQLModel, Field


class Order(SQLModel, table=True):
    """Orders."""

    __tablename__ = "orders"

    id: int | None = Field(primary_key=True, default=None)
    seat_id: int = Field(sa_column=Column(INTEGER))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    transaction_id: str | None = Field(sa_column=Column(VARCHAR(255)), default=None)
    payment_method: str | None = Field(sa_column=Column(VARCHAR(64)), default=None)
    status: str = Field(sa_column=Column(VARCHAR(64)), default="created")
    total_cost: int = Field(sa_column=Column(INTEGER), default=0)
