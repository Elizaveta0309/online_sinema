"""empty message

Revision ID: c24531f9bfc3
Revises: a7580e4428df
Create Date: 2023-04-29 12:21:30.252217

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c24531f9bfc3'
down_revision = 'a7580e4428df'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_social',
    sa.Column('user', sa.UUID(), nullable=False),
    sa.Column('social_user_id', sa.String(length=255), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['user'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_unique_constraint(None, 'account_entrance', ['id'])
    op.create_unique_constraint(None, 'refresh_token', ['id'])
    op.create_unique_constraint(None, 'role', ['id'])
    op.create_unique_constraint(None, 'user', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_constraint(None, 'role', type_='unique')
    op.drop_constraint(None, 'refresh_token', type_='unique')
    op.drop_constraint(None, 'account_entrance', type_='unique')
    op.drop_table('user_social')
    # ### end Alembic commands ###
