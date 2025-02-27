"""empty message

Revision ID: 3d1571e92915
Revises: 7bbc41fc98fe
Create Date: 2025-02-26 10:22:29.026776

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3d1571e92915'
down_revision: Union[str, None] = '7bbc41fc98fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'first_name',
               existing_type=sa.VARCHAR(length=16),
               type_=sa.String(length=64),
               existing_nullable=False)
    op.alter_column('users', 'last_name',
               existing_type=sa.VARCHAR(length=16),
               type_=sa.String(length=64),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'last_name',
               existing_type=sa.String(length=64),
               type_=sa.VARCHAR(length=16),
               existing_nullable=False)
    op.alter_column('users', 'first_name',
               existing_type=sa.String(length=64),
               type_=sa.VARCHAR(length=16),
               existing_nullable=False)
    # ### end Alembic commands ###
