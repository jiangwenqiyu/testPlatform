"""empty message

Revision ID: 729d80cc1e78
Revises: 73eea307f5e7
Create Date: 2022-03-30 17:13:55.068680

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '729d80cc1e78'
down_revision = '73eea307f5e7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('createTime', sa.DateTime(), nullable=True),
    sa.Column('updateTime', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('user', sa.Column('account', sa.String(length=20), nullable=False))
    op.add_column('user', sa.Column('role_id', sa.String(length=20), nullable=False))
    op.drop_index('name', table_name='user')
    op.create_unique_constraint(None, 'user', ['account'])
    op.drop_column('user', 'role')
    op.drop_column('user', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('name', mysql.VARCHAR(length=20), nullable=False))
    op.add_column('user', sa.Column('role', mysql.VARCHAR(length=20), nullable=False))
    op.drop_constraint(None, 'user', type_='unique')
    op.create_index('name', 'user', ['name'], unique=False)
    op.drop_column('user', 'role_id')
    op.drop_column('user', 'account')
    op.drop_table('role')
    # ### end Alembic commands ###
