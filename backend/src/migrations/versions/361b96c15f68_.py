"""empty message

Revision ID: 361b96c15f68
Revises: 4ebcb7d870e8
Create Date: 2025-03-08 10:40:12.896830

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '361b96c15f68'
down_revision: Union[str, None] = '4ebcb7d870e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('calendar_tasks', sa.Column('uuid', sa.Uuid(), nullable=False))
    op.drop_column('calendar_tasks', 'id')
    op.add_column('todolist', sa.Column('uuid', sa.Uuid(), nullable=False))
    op.drop_column('todolist', 'id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todolist', sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.drop_column('todolist', 'uuid')
    op.add_column('calendar_tasks', sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.drop_column('calendar_tasks', 'uuid')
    # ### end Alembic commands ###
