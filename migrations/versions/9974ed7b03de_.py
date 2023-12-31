"""empty message

Revision ID: 9974ed7b03de
Revises: 
Create Date: 2023-09-28 01:26:19.813279

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9974ed7b03de'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('movies')
    op.drop_table('tokens')
    op.drop_table('revoked_tokens')
    op.drop_table('blacklist_tokens')
    op.drop_table('users')
    op.drop_table('genres')
    op.drop_table('blacklisted_tokens')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blacklisted_tokens',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('jwt', sa.VARCHAR(length=255), nullable=False),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('jwt')
    )
    op.create_table('genres',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), nullable=False),
    sa.Column('movie_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=50), nullable=False),
    sa.Column('password', sa.VARCHAR(length=60), nullable=False),
    sa.Column('role', sa.VARCHAR(length=10), nullable=True),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('blacklist_tokens',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('token', sa.VARCHAR(length=500), nullable=False),
    sa.Column('blacklisted_on', sa.DATETIME(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token')
    )
    op.create_table('revoked_tokens',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('jti', sa.VARCHAR(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('jti')
    )
    op.create_table('tokens',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('token', sa.VARCHAR(length=255), nullable=False),
    sa.Column('token_type', sa.VARCHAR(length=50), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('movies',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), nullable=False),
    sa.Column('director', sa.VARCHAR(length=100), nullable=False),
    sa.Column('popularity', sa.FLOAT(), nullable=False),
    sa.Column('imdb_score', sa.FLOAT(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
