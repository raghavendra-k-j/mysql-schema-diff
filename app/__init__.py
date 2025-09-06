"""MySQL Schema Diff Reporter package."""
from .db import DatabaseConnection, ColumnInfo
from .diff import SchemaDiff, TableDiff, compute_schema_diff
from .render_markdown import build_markdown
from .render_html import build_html

__version__ = "1.0.0"
__all__ = [
    'DatabaseConnection',
    'ColumnInfo',
    'SchemaDiff',
    'TableDiff',
    'compute_schema_diff',
    'build_markdown',
    'build_html'
]
