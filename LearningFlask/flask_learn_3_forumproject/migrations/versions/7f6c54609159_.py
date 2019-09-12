"""empty message

Revision ID: 7f6c54609159
Revises: e9e70a0e9df1
Create Date: 2019-04-03 14:25:03.384190

"""

# revision identifiers, used by Alembic.
revision = '7f6c54609159'
down_revision = 'e9e70a0e9df1'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('roles', sa.Column('default', sa.Boolean(), nullable=True))
    op.add_column('roles', sa.Column('permission', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_roles_default'), 'roles', ['default'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_roles_default'), table_name='roles')
    op.drop_column('roles', 'permission')
    op.drop_column('roles', 'default')
    # ### end Alembic commands ###
