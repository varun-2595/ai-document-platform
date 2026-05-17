"""Baseline the original documents table."""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20260518_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "documents",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("filename", sa.String(), nullable=False),
        sa.Column("upload_time", sa.DateTime()),
    )
    op.create_index("ix_documents_id", "documents", ["id"])


def downgrade() -> None:
    op.drop_index("ix_documents_id", table_name="documents")
    op.drop_table("documents")
