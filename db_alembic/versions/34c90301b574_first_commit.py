"""First commit

Revision ID: 34c90301b574
Revises: 
Create Date: 2022-12-27 07:27:43.369575

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34c90301b574'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_comments_id'), 'comments', ['id'], unique=False)
    op.create_index(op.f('ix_postResponses_id'), 'postResponses', ['id'], unique=False)
    op.add_column('users', sa.Column('username', sa.String(length=100), nullable=False))
    op.create_unique_constraint(None, 'users', ['username'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'username')
    op.drop_index(op.f('ix_postResponses_id'), table_name='postResponses')
    op.drop_index(op.f('ix_comments_id'), table_name='comments')
    # ### end Alembic commands ###