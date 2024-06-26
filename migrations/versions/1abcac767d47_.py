"""empty message

Revision ID: 1abcac767d47
Revises: 22a2b3738333
Create Date: 2024-06-04 08:41:45.047649

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import src


# revision identifiers, used by Alembic.
revision: str = '1abcac767d47'
down_revision: Union[str, None] = '22a2b3738333'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('book_private_tags_book_private_id_fkey', 'book_private_tags', type_='foreignkey')
    op.create_foreign_key(None, 'book_private_tags', 'books_private', ['book_private_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.alter_column('books_private', 'slug',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('books_private', 'slug',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.drop_constraint(None, 'book_private_tags', type_='foreignkey')
    op.create_foreign_key('book_private_tags_book_private_id_fkey', 'book_private_tags', 'books_private', ['book_private_id'], ['id'], onupdate='CASCADE', ondelete='RESTRICT')
    # ### end Alembic commands ###
