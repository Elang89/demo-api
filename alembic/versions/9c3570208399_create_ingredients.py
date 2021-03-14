"""create ingredients

Revision ID: 9c3570208399
Revises: c3c73cbd4948
Create Date: 2021-03-09 20:24:05.465384

"""
from alembic import op

import sqlalchemy as sa
import uuid
import datetime
import sys

sys.path = ["", ".."] + sys.path[1:]

from app.models.custom import GUID

# revision identifiers, used by Alembic.
revision = "9c3570208399"
down_revision = "c3c73cbd4948"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "ingredients",
        sa.Column("id", GUID(), default=uuid.uuid4, primary_key=True),
        sa.Column("name", sa.String(50), nullable=False, unique=True),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column(
            "created_at", sa.DateTime, nullable=False, default=datetime.datetime.utcnow
        ),
        sa.Column("updated_at", sa.DateTime, nullable=True),
    )


def downgrade():
    op.drop_table("ingredients")
