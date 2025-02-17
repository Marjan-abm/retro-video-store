"""empty message

Revision ID: 63ac0a2dc2aa
Revises: dfad7fca53c8
Create Date: 2021-11-09 21:30:09.050938

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63ac0a2dc2aa'
down_revision = 'dfad7fca53c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('videos', 'available_inventory')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('videos', sa.Column('available_inventory', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
