"""Schema difference calculation module."""
from typing import Dict, Set, NamedTuple, Optional
from dataclasses import dataclass
from .db import ColumnInfo

@dataclass
class TableDiff:
    """Represents column differences for a single table."""
    added_columns: Dict[str, ColumnInfo]
    removed_columns: Dict[str, ColumnInfo]

    @property
    def has_changes(self) -> bool:
        """Return True if the table has any column changes."""
        return bool(self.added_columns or self.removed_columns)

@dataclass
class SchemaDiff:
    """Represents overall schema differences between two databases."""
    added_tables: Set[str]
    removed_tables: Set[str]
    changed_tables: Dict[str, TableDiff]

    @property
    def has_changes(self) -> bool:
        """Return True if there are any schema changes."""
        return bool(
            self.added_tables or 
            self.removed_tables or 
            any(diff.has_changes for diff in self.changed_tables.values())
        )

def diff_tables(old_tables: Set[str], new_tables: Set[str]) -> tuple[Set[str], Set[str], Set[str]]:
    """Compare table sets to find added, removed, and common tables."""
    added = new_tables - old_tables
    removed = old_tables - new_tables
    common = old_tables & new_tables
    return added, removed, common

def diff_columns(
    table: str,
    old_cols: Dict[str, ColumnInfo],
    new_cols: Dict[str, ColumnInfo]
) -> TableDiff:
    """Compare columns between old and new versions of a table."""
    old_names = set(old_cols.keys())
    new_names = set(new_cols.keys())
    
    added = new_names - old_names
    removed = old_names - new_names
    
    return TableDiff(
        added_columns={name: new_cols[name] for name in added},
        removed_columns={name: old_cols[name] for name in removed}
    )

def compute_schema_diff(
    old_tables: Set[str],
    new_tables: Set[str],
    old_columns: Dict[str, Dict[str, ColumnInfo]],
    new_columns: Dict[str, Dict[str, ColumnInfo]]
) -> SchemaDiff:
    """Compute the complete schema difference between two databases."""
    added_tables, removed_tables, common_tables = diff_tables(old_tables, new_tables)
    
    # Compare columns for common tables
    changed_tables: Dict[str, TableDiff] = {}
    for table in common_tables:
        table_diff = diff_columns(
            table,
            old_columns.get(table, {}),
            new_columns.get(table, {})
        )
        if table_diff.has_changes:
            changed_tables[table] = table_diff
    
    return SchemaDiff(
        added_tables=added_tables,
        removed_tables=removed_tables,
        changed_tables=changed_tables
    )
