"""add_intent_analysis_columns

Revision ID: 73d7a3dc39d6
Revises: 31475a41f572
Create Date: 2024-10-30 15:49:59.262884

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '73d7a3dc39d6'
down_revision = '31475a41f572'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('websites', schema=None) as batch_op:
        batch_op.add_column(sa.Column('intent_question', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('intent_options', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('last_analyzed', sa.DateTime(), nullable=True))
        batch_op.drop_column('last_generated')
        batch_op.drop_column('meta_description')
        batch_op.drop_column('related_topics')
        batch_op.drop_column('keywords')
        batch_op.drop_column('summary')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('websites', schema=None) as batch_op:
        batch_op.add_column(sa.Column('summary', sa.TEXT(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('keywords', sa.TEXT(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('related_topics', sa.TEXT(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('meta_description', sa.TEXT(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('last_generated', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
        batch_op.drop_column('last_analyzed')
        batch_op.drop_column('intent_options')
        batch_op.drop_column('intent_question')

    # ### end Alembic commands ###
