"""empty message

Revision ID: bda292324205
Revises: 00c656809f58
Create Date: 2022-04-08 14:30:03.089043

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'bda292324205'
down_revision = '00c656809f58'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('exe_case_record_detail', 'caseName',
               existing_type=mysql.VARCHAR(length=10),
               type_=sa.String(length=50),
               nullable=False,
               existing_comment='用例名称')
    op.alter_column('exe_case_record_detail', 'consume',
               existing_type=mysql.VARCHAR(length=10),
               type_=sa.String(length=15),
               existing_comment='请求耗时',
               existing_nullable=True)
    op.alter_column('test_case', 'name',
               existing_type=mysql.VARCHAR(length=20),
               type_=sa.String(length=50),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('test_case', 'name',
               existing_type=sa.String(length=50),
               type_=mysql.VARCHAR(length=20),
               existing_nullable=False)
    op.alter_column('exe_case_record_detail', 'consume',
               existing_type=sa.String(length=15),
               type_=mysql.VARCHAR(length=10),
               existing_comment='请求耗时',
               existing_nullable=True)
    op.alter_column('exe_case_record_detail', 'caseName',
               existing_type=sa.String(length=50),
               type_=mysql.VARCHAR(length=10),
               nullable=True,
               existing_comment='用例名称')
    # ### end Alembic commands ###
