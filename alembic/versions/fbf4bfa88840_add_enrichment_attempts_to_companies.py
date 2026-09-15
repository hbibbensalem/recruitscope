"""add enrichment_attempts to companies

Revision ID: fbf4bfa88840
Revises: 2e9f9e4b187f
Create Date: 2026-09-15 17:38:33.696551

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fbf4bfa88840'
down_revision: Union[str, Sequence[str], None] = '2e9f9e4b187f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'companies',
        sa.Column('enrichment_attempts', sa.Integer(), nullable=False, server_default='0')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('companies', 'enrichment_attempts')