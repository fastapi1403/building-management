"""Add fund_transactions relationship to Charge model

Revision ID: aaa83521e3f7
Revises: 9514ffad2eea
Create Date: 2025-01-17 09:40:29.299032

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'aaa83521e3f7'
down_revision: Union[str, None] = '9514ffad2eea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
