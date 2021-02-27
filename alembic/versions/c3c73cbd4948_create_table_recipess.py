"""create table recipess

Revision ID: c3c73cbd4948
Revises: 
Create Date: 2021-02-24 22:41:59.411604

"""
from alembic import op

import sqlalchemy as sa
import uuid
import datetime

from app.models.custom import GUID


# revision identifiers, used by Alembic.
revision = "c3c73cbd4948"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "recipes",
        sa.Column("id", GUID(), default=uuid.uuid4, primary_key=True),
        sa.Column("name", sa.String(50), nullable=False, unique=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column(
            "created_at", sa.DateTime, nullable=False, default=datetime.datetime.utcnow
        ),
        sa.Column("updated_at", sa.DateTime, nullable=True),
    )


def downgrade():
    op.drop_table("recipes")
