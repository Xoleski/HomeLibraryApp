"""empty message

Revision ID: 1df69d92d272
Revises: 74615edcf57c
Create Date: 2024-05-14 14:40:25.680927

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import src


# revision identifiers, used by Alembic.
revision: str = '1df69d92d272'
down_revision: Union[str, None] = '74615edcf57c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('article_tags_article_id_fkey', 'article_tags', type_='foreignkey')
    op.create_foreign_key(None, 'article_tags', 'articles', ['article_id'], ['id'], onupdate='CASCADE', ondelete='RESTRICT')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'article_tags', type_='foreignkey')
    op.create_foreign_key('article_tags_article_id_fkey', 'article_tags', 'general_books', ['article_id'], ['id'], onupdate='CASCADE', ondelete='RESTRICT')
    # ### end Alembic commands ###
