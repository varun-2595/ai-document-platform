"""Harden ingestion and add chunks."""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20260518_0002"
down_revision: Union[str, None] = "20260518_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("documents", "filename", new_column_name="original_filename")
    op.alter_column("documents", "upload_time", new_column_name="created_at")
    op.add_column("documents", sa.Column("storage_path", sa.String(length=512)))
    op.add_column("documents", sa.Column("content_type", sa.String(length=128)))
    op.add_column("documents", sa.Column("size_bytes", sa.BigInteger()))
    op.add_column("documents", sa.Column("status", sa.String(length=32), nullable=False, server_default="uploaded"))
    op.add_column("documents", sa.Column("error_message", sa.Text()))
    op.add_column("documents", sa.Column("extracted_text", sa.Text()))
    op.add_column("documents", sa.Column("page_count", sa.Integer()))
    op.add_column("documents", sa.Column("ocr_required", sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column("documents", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()))
    op.execute(
        """
        UPDATE documents
        SET storage_path = 'legacy/' || id::text,
            content_type = 'application/pdf',
            size_bytes = 0,
            created_at = COALESCE(created_at, NOW())
        """
    )
    op.alter_column("documents", "storage_path", nullable=False)
    op.alter_column("documents", "content_type", nullable=False)
    op.alter_column("documents", "size_bytes", nullable=False)
    op.alter_column("documents", "created_at", nullable=False)
    op.create_unique_constraint("uq_documents_storage_path", "documents", ["storage_path"])
    op.create_table(
        "document_chunks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("document_id", sa.Integer(), sa.ForeignKey("documents.id", ondelete="CASCADE"), nullable=False),
        sa.Column("chunk_index", sa.Integer(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("token_count", sa.Integer(), nullable=False),
        sa.Column("embedding_id", sa.String(length=255)),
        sa.Column("chunking_version", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("document_id", "chunk_index", name="uq_document_chunk_position"),
    )
    op.create_index("ix_document_chunks_id", "document_chunks", ["id"])
    op.create_index("ix_document_chunks_document_id", "document_chunks", ["document_id"])


def downgrade() -> None:
    op.drop_index("ix_document_chunks_document_id", table_name="document_chunks")
    op.drop_index("ix_document_chunks_id", table_name="document_chunks")
    op.drop_table("document_chunks")
    op.drop_constraint("uq_documents_storage_path", "documents", type_="unique")
    op.drop_column("documents", "updated_at")
    op.drop_column("documents", "ocr_required")
    op.drop_column("documents", "page_count")
    op.drop_column("documents", "extracted_text")
    op.drop_column("documents", "error_message")
    op.drop_column("documents", "status")
    op.drop_column("documents", "size_bytes")
    op.drop_column("documents", "content_type")
    op.drop_column("documents", "storage_path")
    op.alter_column("documents", "created_at", new_column_name="upload_time")
    op.alter_column("documents", "original_filename", new_column_name="filename")
