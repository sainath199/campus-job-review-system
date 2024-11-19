"""Add user_activity table

Revision ID: add_user_activity_table
Revises: cf22d1ca3bbc
Create Date: 2024-11-19 10:00:00
"""

from alembic import op
import sqlalchemy as sa

# Revision identifiers
revision = 'add_user_activity_table'
down_revision = 'cf22d1ca3bbc'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user_activity',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('vacancy_id', sa.Integer(), sa.ForeignKey('vacancies.vacancyId'), nullable=False),
        sa.Column('status', sa.Enum('applied', 'interview', 'offer', name='activity_status'), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False, server_default=sa.func.now())
    )


def downgrade():
    op.drop_table('user_activity')
    op.execute('DROP TYPE activity_status')

