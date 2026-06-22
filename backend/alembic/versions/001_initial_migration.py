"""create initial migration

Revision ID: 001
Revises: 
Create Date: 2026-06-22 04:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create users table
    op.create_table('users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('username', sa.String(100), nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('full_name', sa.String(255), nullable=True),
        sa.Column('phone', sa.String(20), nullable=True),
        sa.Column('role', sa.Enum('donor', 'admin', 'staff', name='userrole'), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_verified', sa.Boolean(), nullable=False),
        sa.Column('preferred_currency', sa.String(3), nullable=False),
        sa.Column('preferred_language', sa.String(5), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('last_login', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)

    # Create missionary_funds table
    op.create_table('missionary_funds',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('goal_amount', sa.Float(), nullable=True),
        sa.Column('current_amount', sa.Float(), nullable=False),
        sa.Column('currency', sa.String(3), nullable=False),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column('image_url', sa.String(500), nullable=True),
        sa.Column('beneficiary_name', sa.String(255), nullable=True),
        sa.Column('beneficiary_country', sa.String(100), nullable=True),
        sa.Column('start_date', sa.DateTime(), nullable=False),
        sa.Column('end_date', sa.DateTime(), nullable=True),
        sa.Column('donor_count', sa.Integer(), nullable=False),
        sa.Column('is_featured', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create donations table
    op.create_table('donations',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('donor_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('fund_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('currency', sa.String(3), nullable=False),
        sa.Column('status', sa.Enum('pending', 'completed', 'failed', 'cancelled', name='donationstatus'), nullable=False),
        sa.Column('payment_method', sa.String(50), nullable=False),
        sa.Column('transaction_id', sa.String(255), nullable=True),
        sa.Column('reference_number', sa.String(255), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('anonymous', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['donor_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['fund_id'], ['missionary_funds.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('reference_number')
    )
    op.create_index(op.f('ix_donations_reference_number'), 'donations', ['reference_number'], unique=True)
    op.create_index(op.f('ix_donations_transaction_id'), 'donations', ['transaction_id'], unique=True)

    # Create donation_receipts table
    op.create_table('donation_receipts',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('donation_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('file_path', sa.String(500), nullable=True),
        sa.Column('file_type', sa.String(20), nullable=True),
        sa.Column('file_size', sa.Float(), nullable=True),
        sa.Column('uploaded_at', sa.DateTime(), nullable=False),
        sa.Column('verified', sa.Boolean(), nullable=False),
        sa.Column('verified_at', sa.DateTime(), nullable=True),
        sa.Column('verified_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(['donation_id'], ['donations.id'], ),
        sa.ForeignKeyConstraint(['verified_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('donation_id')
    )

    # Create payment_methods table
    op.create_table('payment_methods',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('country_code', sa.String(2), nullable=False),
        sa.Column('bank_name', sa.String(255), nullable=False),
        sa.Column('account_holder', sa.String(255), nullable=False),
        sa.Column('account_number', sa.String(50), nullable=True),
        sa.Column('bank_code', sa.String(10), nullable=True),
        sa.Column('swift_code', sa.String(20), nullable=True),
        sa.Column('currency', sa.String(3), nullable=False),
        sa.Column('qr_code_data', sa.String(500), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create bank_transfers table
    op.create_table('bank_transfers',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('payment_method_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('currency', sa.String(3), nullable=False),
        sa.Column('reference_number', sa.String(255), nullable=False),
        sa.Column('qr_code_image', sa.String(500), nullable=True),
        sa.Column('instructions', sa.String(1000), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('reference_number')
    )
    op.create_index(op.f('ix_bank_transfers_reference_number'), 'bank_transfers', ['reference_number'], unique=True)

def downgrade() -> None:
    op.drop_index(op.f('ix_bank_transfers_reference_number'), table_name='bank_transfers')
    op.drop_table('bank_transfers')
    op.drop_table('payment_methods')
    op.drop_table('donation_receipts')
    op.drop_index(op.f('ix_donations_transaction_id'), table_name='donations')
    op.drop_index(op.f('ix_donations_reference_number'), table_name='donations')
    op.drop_table('donations')
    op.drop_table('missionary_funds')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
