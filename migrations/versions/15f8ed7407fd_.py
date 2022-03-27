"""empty message

Revision ID: 15f8ed7407fd
Revises: 44ddc8093e68
Create Date: 2022-03-27 16:53:53.492982

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15f8ed7407fd'
down_revision = '44ddc8093e68'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('test_case', sa.Column('status', sa.Integer(), nullable=True, comment='当前用例状态 0 就绪  1 进行中  2  成功  3  失败'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('test_case', 'status')
    # ### end Alembic commands ###
