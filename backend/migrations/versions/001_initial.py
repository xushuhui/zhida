"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2023-07-20 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('password', sa.String(255), nullable=False),
        sa.Column('avatar', sa.String(255), nullable=True),
        sa.Column('role', sa.Enum('admin', 'user', name='user_roles'), nullable=False, server_default='user'),
        sa.Column('status', sa.Enum('active', 'disabled', name='user_status'), nullable=False, server_default='active'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.Column('last_login', sa.DateTime(), nullable=True),
        sa.Column('preferences', sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('email')
    )
    op.create_index('idx_users_created_at', 'users', ['created_at'], unique=False)

    # Create sessions table
    op.create_table('sessions',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('status', sa.Enum('active', 'archived', name='session_status'), nullable=False, server_default='active'),
        sa.Column('message_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('last_message_time', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.Column('system_prompt', sa.Text(), nullable=True),
        sa.Column('temperature', sa.DECIMAL(3,2), nullable=True),
        sa.Column('max_tokens', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_sessions_user_id', 'sessions', ['user_id'], unique=False)
    op.create_index('idx_sessions_created_at', 'sessions', ['created_at'], unique=False)
    op.create_index('idx_sessions_last_message', 'sessions', ['last_message_time'], unique=False)

    # Create messages table
    op.create_table('messages',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('session_id', sa.BigInteger(), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('role', sa.Enum('user', 'assistant', 'system', name='message_roles'), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('tokens', sa.Integer(), nullable=True),
        sa.Column('status', sa.Enum('sent', 'delivered', 'error', name='message_status'), nullable=False, server_default='sent'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('response_time', sa.Integer(), nullable=True),
        sa.Column('client_info', sa.String(255), nullable=True),
        sa.Column('ip_address', sa.String(45), nullable=True),
        sa.ForeignKeyConstraint(['session_id'], ['sessions.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_messages_session', 'messages', ['session_id'], unique=False)
    op.create_index('idx_messages_user', 'messages', ['user_id'], unique=False)
    op.create_index('idx_messages_created', 'messages', ['created_at'], unique=False)
    op.create_index('idx_messages_role', 'messages', ['role'], unique=False)

    # Create statistics table
    op.create_table('statistics',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('chat_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('message_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('avg_response_time', sa.Float(), nullable=True),
        sa.Column('token_usage', sa.BigInteger(), nullable=False, server_default='0'),
        sa.Column('error_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_statistics_date', 'statistics', ['date'], unique=False)
    op.create_unique_constraint('unique_user_date', 'statistics', ['user_id', 'date'])


def downgrade() -> None:
    op.drop_table('statistics')
    op.drop_table('messages')
    op.drop_table('sessions')
    op.drop_table('users')