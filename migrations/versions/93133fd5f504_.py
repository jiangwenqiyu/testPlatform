"""empty message

Revision ID: 93133fd5f504
Revises: bda292324205
Create Date: 2022-04-14 21:47:45.843647

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '93133fd5f504'
down_revision = 'bda292324205'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'role_id',
               existing_type=mysql.VARCHAR(length=20),
               nullable=True)
    op.create_foreign_key(None, 'user', 'role', ['role_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.alter_column('user', 'role_id',
               existing_type=mysql.VARCHAR(length=20),
               nullable=False)
    # ### end Alembic commands ###
