"""create_recipes_ingredients

Revision ID: 7d497eb3bfa7
Revises: 9c3570208399
Create Date: 2021-03-09 20:30:42.650146

"""
from alembic import op
from sqlalchemy import ForeignKey

import sqlalchemy as sa
import sys


# revision identifiers, used by Alembic.
revision = "7d497eb3bfa7"
down_revision = "9c3570208399"
branch_labels = None
depends_on = None

sys.path = ["", ".."] + sys.path[1:]

from app.models.custom import GUID


def upgrade():
    op.create_table(
        "recipes_ingredients",
        sa.Column(
            "recipe_id",
            GUID(),
            ForeignKey("recipes.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "ingredient_id",
            GUID(),
            ForeignKey("ingredients.id", ondelete="CASCADE"),
            primary_key=True,
        ),
    )


def downgrade():
    op.drop_table("recipes_ingredients")
