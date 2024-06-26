"""empty message

Revision ID: 2d524970f437
Revises: cb2e4aac0d18
Create Date: 2024-05-28 21:34:56.636281

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import src


# revision identifiers, used by Alembic.
revision: str = '2d524970f437'
down_revision: Union[str, None] = 'cb2e4aac0d18'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('books_private', 'picture')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books_private', sa.Column('picture', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
