"""add constraint to cart table

Revision ID: 64f3b4ab399c
Revises: d4b5322267db
Create Date: 2024-09-14 18:02:12.980351

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '64f3b4ab399c'
down_revision: Union[str, None] = 'd4b5322267db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'cart', ['user_id', 'item_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'cart', type_='unique')
    # ### end Alembic commands ###
