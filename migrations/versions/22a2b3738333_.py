"""empty message

Revision ID: 22a2b3738333
Revises: df6aa891d00d
Create Date: 2024-06-01 19:53:26.461059

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import src


# revision identifiers, used by Alembic.
revision: str = '22a2b3738333'
down_revision: Union[str, None] = 'df6aa891d00d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('books_private', 'slug',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.drop_constraint('books_private_slug_key', 'books_private', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('books_private_slug_key', 'books_private', ['slug'])
    op.alter_column('books_private', 'slug',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    # ### end Alembic commands ###
