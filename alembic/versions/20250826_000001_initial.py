"""initial schema

Revision ID: 20250826_000001
Revises:
Create Date: 2025-08-26 00:00:01

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '20250826_000001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # users
    op.create_table(
        'users',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('email', sa.Text(), nullable=False, unique=True),
        sa.Column('password_hash', sa.Text(), nullable=False),
        sa.Column('plan', sa.Text(), nullable=False, server_default=sa.text("'free'")),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
    )

    # sources
    op.create_table(
        'sources',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.BigInteger(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('type', sa.Text(), nullable=False),
        sa.Column('url', sa.Text(), nullable=False),
        sa.Column('tags', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column('crawl_interval_m', sa.Integer(), nullable=False, server_default=sa.text('60')),
        sa.Column('enabled', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('last_crawled_at', sa.TIMESTAMP(timezone=True)),
        sa.CheckConstraint("type in ('rss','site','api')", name='sources_type_check'),
    )
    op.create_index('idx_sources_user', 'sources', ['user_id'])

    # documents
    op.create_table(
        'documents',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.BigInteger(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('source_id', sa.BigInteger(), sa.ForeignKey('sources.id', ondelete='SET NULL')),
        sa.Column('url', sa.Text(), nullable=False),
        sa.Column('title', sa.Text()),
        sa.Column('author', sa.Text()),
        sa.Column('published_at', sa.TIMESTAMP(timezone=True)),
        sa.Column('ingested_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('hash', sa.Text()),
        sa.Column('status', sa.Text(), nullable=False, server_default=sa.text("'new'")),
        sa.Column('lang', sa.Text()),
        sa.Column('tags', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.UniqueConstraint('user_id', 'url', name='uq_documents_user_url'),
        sa.CheckConstraint("status in ('new','embedded','error')", name='documents_status_check'),
    )
    op.create_index('idx_documents_user', 'documents', ['user_id'])
    op.create_index('idx_documents_source', 'documents', ['source_id'])
    op.create_index('idx_documents_status', 'documents', ['status'])

    # chunks
    op.create_table(
        'chunks',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.BigInteger(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('document_id', sa.BigInteger(), sa.ForeignKey('documents.id', ondelete='CASCADE'), nullable=False),
        sa.Column('chunk_index', sa.Integer(), nullable=False),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('token_count', sa.Integer()),
        sa.Column('embedding_ref', sa.Text()),
        sa.Column('metadata_json', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.UniqueConstraint('document_id', 'chunk_index', name='uq_chunks_doc_idx'),
    )
    op.create_index('idx_chunks_doc', 'chunks', ['document_id'])
    op.create_index('idx_chunks_user', 'chunks', ['user_id'])

    # digests
    op.create_table(
        'digests',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.BigInteger(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('date_utc', sa.Date(), nullable=False),
        sa.Column('headline', sa.Text()),
        sa.Column('bullets_json', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column('model', sa.Text()),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.UniqueConstraint('user_id', 'date_utc', name='uq_digests_user_date'),
    )
    op.create_index('idx_digests_user_date', 'digests', ['user_id', 'date_utc'])

    # votes
    op.create_table(
        'votes',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.BigInteger(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('target_type', sa.Text(), nullable=False),
        sa.Column('target_id', sa.Text(), nullable=False),
        sa.Column('vote', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.CheckConstraint("vote in (-1,0,1)", name='votes_vote_check'),
        sa.CheckConstraint("target_type in ('digest_bullet','doc','answer_snippet')", name='votes_type_check'),
    )
    op.create_index('idx_votes_user', 'votes', ['user_id'])
    op.create_index('idx_votes_target', 'votes', ['target_type', 'target_id'])

    # queries
    op.create_table(
        'queries',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.BigInteger(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('query_text', sa.Text(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
    )
    op.create_index('idx_queries_user', 'queries', ['user_id'])

    # preferences
    op.create_table(
        'preferences',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.BigInteger(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('tag', sa.Text(), nullable=False),
        sa.Column('weight', sa.Float(), nullable=False, server_default=sa.text('0')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.UniqueConstraint('user_id', 'tag', name='uq_preferences_user_tag'),
    )
    op.create_index('idx_preferences_user', 'preferences', ['user_id'])

    # trends
    op.create_table(
        'trends',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.BigInteger(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('metric', sa.Text(), nullable=False),
        sa.Column('time_window', sa.Text(), nullable=False),
        sa.Column('tag', sa.Text(), nullable=False),
        sa.Column('value', sa.Float(), nullable=False),
        sa.Column('computed_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.CheckConstraint("time_window in ('15m','1h','24h')", name='trends_time_window_check'),
    )
    op.create_index('idx_trends_user_metric', 'trends', ['user_id', 'metric', 'time_window'])
    op.create_index('idx_trends_tag', 'trends', ['tag'])


def downgrade() -> None:
    op.drop_index('idx_trends_tag', table_name='trends')
    op.drop_index('idx_trends_user_metric', table_name='trends')
    op.drop_table('trends')

    op.drop_index('idx_preferences_user', table_name='preferences')
    op.drop_table('preferences')

    op.drop_index('idx_queries_user', table_name='queries')
    op.drop_table('queries')

    op.drop_index('idx_votes_target', table_name='votes')
    op.drop_index('idx_votes_user', table_name='votes')
    op.drop_table('votes')

    op.drop_index('idx_digests_user_date', table_name='digests')
    op.drop_table('digests')

    op.drop_index('idx_chunks_user', table_name='chunks')
    op.drop_index('idx_chunks_doc', table_name='chunks')
    op.drop_table('chunks')

    op.drop_index('idx_documents_status', table_name='documents')
    op.drop_index('idx_documents_source', table_name='documents')
    op.drop_index('idx_documents_user', table_name='documents')
    op.drop_table('documents')

    op.drop_index('idx_sources_user', table_name='sources')
    op.drop_table('sources')

    op.drop_table('users')
