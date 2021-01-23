"""empty message

Revision ID: be8a4371016d
Revises: ab65fd5bf21b
Create Date: 2021-01-24 00:24:13.912189

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be8a4371016d'
down_revision = 'ab65fd5bf21b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('artists_genres',
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('genre_name', sa.String(length=60), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['artists.id'], ),
    sa.ForeignKeyConstraint(['genre_name'], ['genres.name'], ),
    sa.PrimaryKeyConstraint('artist_id', 'genre_name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('artists_genres')
    # ### end Alembic commands ###