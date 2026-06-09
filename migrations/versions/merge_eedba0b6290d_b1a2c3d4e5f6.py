"""merge heads

Revision ID: merge_eedba0b6290d_b1a2c3d4e5f6
Revises: eedba0b6290d, b1a2c3d4e5f6
Create Date: 2026-06-09 15:45:00.000000

"""

from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = "merge_eedba0b6290d_b1a2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = (
    "eedba0b6290d",
    "b1a2c3d4e5f6",
)
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # merge-only revision.
    pass


def downgrade() -> None:
    pass
