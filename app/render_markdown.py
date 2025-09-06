"""Markdown report generation module."""
from datetime import datetime
from typing import List
from .diff import SchemaDiff, TableDiff

def format_column_info(column_name: str, info) -> str:
    """Format column information into a readable string."""
    parts = [
        f"`{column_name}`",
        f"`{info.column_type}`",
        "NULL" if info.is_nullable == "YES" else "NOT NULL"
    ]
    
    if info.column_default is not None:
        parts.append(f"DEFAULT {info.column_default}")
    if info.column_key:
        parts.append(info.column_key)
    if info.extra:
        parts.append(info.extra)
        
    return " ".join(parts)

def build_markdown(diff: SchemaDiff) -> str:
    """Generate a Markdown report from schema differences."""
    lines: List[str] = []
    
    # Header
    lines.extend([
        "# MySQL Schema Diff Report",
        f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        ""
    ])
    
    # Summary
    summary = []
    if diff.added_tables:
        summary.append(f"+{len(diff.added_tables)} tables")
    if diff.removed_tables:
        summary.append(f"-{len(diff.removed_tables)} tables")
    if diff.changed_tables:
        summary.append(f"{len(diff.changed_tables)} tables changed")
    
    if summary:
        lines.extend([
            "## Summary",
            ", ".join(summary),
            ""
        ])
    
    # Added Tables
    lines.append("## Added Tables")
    if diff.added_tables:
        for table in sorted(diff.added_tables):
            lines.append(f"- `{table}`")
    else:
        lines.append("_None_")
    lines.append("")
    
    # Removed Tables
    lines.append("## Removed Tables")
    if diff.removed_tables:
        for table in sorted(diff.removed_tables):
            lines.append(f"- `{table}`")
    else:
        lines.append("_None_")
    lines.append("")
    
    # Column Changes
    if diff.changed_tables:
        lines.append("## Column Changes")
        for table_name in sorted(diff.changed_tables.keys()):
            table_diff = diff.changed_tables[table_name]
            lines.extend([
                f"### {table_name}",
                ""
            ])
            
            if table_diff.added_columns:
                lines.append("Added columns:")
                for col_name, col_info in sorted(table_diff.added_columns.items()):
                    lines.append(f"- {format_column_info(col_name, col_info)}")
                lines.append("")
                
            if table_diff.removed_columns:
                lines.append("Removed columns:")
                for col_name, col_info in sorted(table_diff.removed_columns.items()):
                    lines.append(f"- {format_column_info(col_name, col_info)}")
                lines.append("")
    else:
        lines.append("## Column Changes")
        lines.append("_None_")
        lines.append("")
    
    return "\n".join(lines)
