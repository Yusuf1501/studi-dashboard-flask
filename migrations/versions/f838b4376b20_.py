"""empty message

Revision ID: f838b4376b20
Revises: 486af05c6bea
Create Date: 2023-11-19 16:17:19.779017

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f838b4376b20'
down_revision = '486af05c6bea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('standard_criteria',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('criterion', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('standard_criteria')
    # ### end Alembic commands ###
