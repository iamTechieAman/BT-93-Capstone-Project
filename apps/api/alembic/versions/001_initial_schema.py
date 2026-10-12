"""Initial schema migration for Smart GST System.

Revision ID: 001_initial_schema
Revises:
Create Date: 2026-10-09
"""

import sqlalchemy as sa

from alembic import op

revision = "001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Users Table
    op.create_table(
        "users",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("role", sa.String(50), nullable=False, default="VIEWER"),
        sa.Column("is_active", sa.Boolean(), nullable=False, default=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )

    # Invoices Table
    op.create_table(
        "invoices",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("invoice_number", sa.String(50), nullable=False, unique=True),
        sa.Column("invoice_date", sa.String(50), nullable=False),
        sa.Column("supplier_gstin", sa.String(15), nullable=False),
        sa.Column("buyer_gstin", sa.String(15), nullable=False),
        sa.Column("place_of_supply", sa.String(50), nullable=False),
        sa.Column("status", sa.String(50), nullable=False, default="FINALIZED"),
        sa.Column("subtotal", sa.Float(), nullable=False),
        sa.Column("cgst_total", sa.Float(), nullable=False, default=0.0),
        sa.Column("sgst_total", sa.Float(), nullable=False, default=0.0),
        sa.Column("igst_total", sa.Float(), nullable=False, default=0.0),
        sa.Column("cess_total", sa.Float(), nullable=False, default=0.0),
        sa.Column("grand_total", sa.Float(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    # Invoice Items Table
    op.create_table(
        "invoice_items",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("invoice_id", sa.String(36), sa.ForeignKey("invoices.id"), nullable=False),
        sa.Column("product_name", sa.String(255), nullable=False),
        sa.Column("hsn_code", sa.String(10), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False, default=1),
        sa.Column("unit_price", sa.Float(), nullable=False),
        sa.Column("taxable_value", sa.Float(), nullable=False),
        sa.Column("gst_rate", sa.Float(), nullable=False),
        sa.Column("cgst_amount", sa.Float(), nullable=False, default=0.0),
        sa.Column("sgst_amount", sa.Float(), nullable=False, default=0.0),
        sa.Column("igst_amount", sa.Float(), nullable=False, default=0.0),
        sa.Column("cess_amount", sa.Float(), nullable=False, default=0.0),
        sa.Column("item_total", sa.Float(), nullable=False),
    )

    # GSTIN Cache Table
    op.create_table(
        "gstin_cache",
        sa.Column("gstin", sa.String(15), primary_key=True),
        sa.Column("legal_name", sa.String(255), nullable=True),
        sa.Column("trade_name", sa.String(255), nullable=True),
        sa.Column("status", sa.String(50), nullable=True),
        sa.Column("registration_date", sa.String(50), nullable=True),
        sa.Column("constitution", sa.String(100), nullable=True),
        sa.Column("jurisdiction", sa.String(255), nullable=True),
        sa.Column("address", sa.String(500), nullable=True),
        sa.Column("provider_name", sa.String(100), nullable=True),
        sa.Column("raw_response", sa.JSON(), nullable=True),
        sa.Column("fetched_at", sa.DateTime(), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
    )

    # Tariff Hierarchy Table
    op.create_table(
        "tariff_hierarchy",
        sa.Column("code", sa.String(10), primary_key=True),
        sa.Column("level", sa.String(20), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "parent_id", sa.String(10), sa.ForeignKey("tariff_hierarchy.code"), nullable=True
        ),
        sa.Column("conditions", sa.JSON(), nullable=True),
        sa.Column("evaluation_factors", sa.JSON(), nullable=True),
    )

    # Tariff Rate Rules Table
    op.create_table(
        "tariff_rate_rules",
        sa.Column("id", sa.String(50), primary_key=True),
        sa.Column("hsn_code", sa.String(10), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("rate", sa.Float(), nullable=False),
        sa.Column("schedule", sa.String(50), nullable=False),
        sa.Column("serial_no", sa.String(50), nullable=False),
        sa.Column("notification_no", sa.String(100), nullable=False),
        sa.Column("notification_date", sa.String(50), nullable=False),
        sa.Column("effective_from", sa.String(50), nullable=False),
        sa.Column("effective_to", sa.String(50), nullable=True),
        sa.Column("source_url", sa.String(500), nullable=False),
        sa.Column("verified_by", sa.String(100), nullable=True),
    )

    # Audit Logs Table
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("action", sa.String(100), nullable=False),
        sa.Column("resource", sa.String(100), nullable=False),
        sa.Column("role", sa.String(50), nullable=False, default="USER"),
        sa.Column("user_id", sa.String(100), nullable=False, default="admin_user"),
        sa.Column("input_data", sa.JSON(), nullable=True),
        sa.Column("output_data", sa.JSON(), nullable=True),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
    )

    # Notification Documents Table
    op.create_table(
        "notification_documents",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("notification_no", sa.String(100), nullable=False, unique=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("category", sa.String(50), nullable=False),
        sa.Column("url", sa.String(500), nullable=False),
        sa.Column("sha256_hash", sa.String(64), nullable=False),
        sa.Column("page_count", sa.Integer(), nullable=False, default=1),
        sa.Column("status", sa.String(50), nullable=False, default="APPROVED"),
        sa.Column("supersedes", sa.String(100), nullable=True),
        sa.Column("fetched_at", sa.DateTime(), nullable=False),
        sa.Column("metadata_json", sa.JSON(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("notification_documents")
    op.drop_table("audit_logs")
    op.drop_table("tariff_rate_rules")
    op.drop_table("tariff_hierarchy")
    op.drop_table("gstin_cache")
    op.drop_table("invoice_items")
    op.drop_table("invoices")
    op.drop_table("users")
