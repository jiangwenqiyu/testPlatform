"""empty message

Revision ID: a15d880176aa
Revises: 06f3237593cd
Create Date: 2022-03-23 21:01:14.851903

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a15d880176aa'
down_revision = '06f3237593cd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('createTime', sa.DateTime(), nullable=True),
    sa.Column('updateTime', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('password', sa.String(length=200), nullable=False),
    sa.Column('role', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.add_column('test_case', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'test_case', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'test_case', type_='foreignkey')
    op.drop_column('test_case', 'user_id')
    op.drop_table('user')
    # ### end Alembic commands ###
