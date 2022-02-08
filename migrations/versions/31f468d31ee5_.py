"""empty message

Revision ID: 31f468d31ee5
Revises: d773ac46ad37
Create Date: 2022-02-07 21:01:47.266524

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31f468d31ee5'
down_revision = 'd773ac46ad37'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pokeparty',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('hp', sa.String(length=50), nullable=True),
    sa.Column('defense', sa.String(length=50), nullable=True),
    sa.Column('attack', sa.String(length=50), nullable=True),
    sa.Column('ability_1', sa.String(length=50), nullable=True),
    sa.Column('ability_2', sa.String(length=50), nullable=True),
    sa.Column('ability_3', sa.String(length=50), nullable=True),
    sa.Column('sprite', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pokeuserjoin',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('poke_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['poke_id'], ['pokeparty.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'poke_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pokeuserjoin')
    op.drop_table('pokeparty')
    # ### end Alembic commands ###
