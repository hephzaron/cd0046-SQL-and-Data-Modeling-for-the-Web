"""empty message

Revision ID: 1a0eb852c33e
Revises: e429be44af7d
Create Date: 2022-05-26 23:45:02.909640

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a0eb852c33e'
down_revision = 'e429be44af7d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column('genres', sa.String(length=120), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('artist', 'genres')
    # ### end Alembic commands ###
