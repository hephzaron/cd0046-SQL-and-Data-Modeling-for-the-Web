"""empty message

Revision ID: ea5bb39794da
Revises: 701e01d7fb83
Create Date: 2022-05-24 00:17:50.745573

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea5bb39794da'
down_revision = '701e01d7fb83'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('venue', 'seeking_description',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('venue', 'seeking_description',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    # ### end Alembic commands ###
