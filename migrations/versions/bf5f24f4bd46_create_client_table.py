"""create client table

Revision ID: bf5f24f4bd46
Revises: 
Create Date: 2022-06-07 17:51:45.242976

"""
from alembic import op
import sqlalchemy as sa

from quotes.adapters.gateway.sql_alchemy.models.client_terminal import ClientTerminal


# revision identifiers, used by Alembic.
revision = 'bf5f24f4bd46'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        ClientTerminal.__tablename__,
        sa.Column("id", sa.String(255), primary_key=True, unique=True, index=True),
        sa.Column("client_name", sa.String(14), unique=True, index=True, nullable=False),
        sa.Column("api_key", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False)    
    )


def downgrade():
    op.drop_table(ClientTerminal.__tablename__)
