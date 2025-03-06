"""empty message

Revision ID: 4ebcb7d870e8
Revises: 7c415754a3fb
Create Date: 2025-03-05 19:44:15.765310

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ebcb7d870e8'
down_revision: Union[str, None] = '7c415754a3fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('users_username_key', 'users', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('users_username_key', 'users', ['username'])
    # ### end Alembic commands ###
