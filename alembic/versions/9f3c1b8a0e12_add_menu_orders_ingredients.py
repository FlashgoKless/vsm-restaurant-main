"""Add menu / ingredients / orders / cooking_tasks

Revision ID: 9f3c1b8a0e12
Revises: 5ad79c711b2f
Create Date: 2026-01-06

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '9f3c1b8a0e12'
down_revision: Union[str, Sequence[str], None] = '5ad79c711b2f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'ingredients',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('stock', sa.Integer(), nullable=False, server_default='0'),
    )

    op.create_table(
        'menu',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('price', sa.Integer(), nullable=False),
        sa.Column('composition', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('is_available', sa.Boolean(), nullable=False, server_default=sa.text('true')),
    )

    op.create_table(
        'orders',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('seat_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('transaction_id', sa.String(length=255), nullable=True),
        sa.Column('payment_method', sa.String(length=64), nullable=True),
        sa.Column('status', sa.String(length=64), nullable=False, server_default=sa.text("'created'")),
        sa.Column('total_cost', sa.Integer(), nullable=False, server_default='0'),
    )

    op.create_table(
        'cooking_tasks',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('order_id', sa.Integer(), nullable=False),
        sa.Column('menu_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('status', sa.String(length=64), nullable=False, server_default=sa.text("'queued'")),
    )


def downgrade() -> None:
    op.drop_table('cooking_tasks')
    op.drop_table('orders')
    op.drop_table('menu')
    op.drop_table('ingredients')
