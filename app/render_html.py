"""HTML report generation module."""
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
from jinja2 import Environment, FileSystemLoader
from .diff import SchemaDiff

def build_html(
    diff: SchemaDiff,
    reviewed_tables: Optional[Dict[str, bool]] = None
) -> str:
    """Generate an HTML report from schema differences."""
    templates_dir = Path(__file__).parent / "templates"
    env = Environment(loader=FileSystemLoader(str(templates_dir)))
    template = env.get_template("report.html.j2")
    
    # Build summary text
    summary_parts = []
    if diff.added_tables:
        summary_parts.append(f"+{len(diff.added_tables)} tables")
    if diff.removed_tables:
        summary_parts.append(f"-{len(diff.removed_tables)} tables")
    if diff.changed_tables:
        summary_parts.append(f"{len(diff.changed_tables)} tables changed")
    summary = ", ".join(summary_parts) if summary_parts else None
    
    return template.render(
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        has_changes=diff.has_changes,
        summary=summary,
        added_tables=diff.added_tables,
        removed_tables=diff.removed_tables,
        changed_tables=diff.changed_tables,
        reviewed=reviewed_tables or {}
    )
