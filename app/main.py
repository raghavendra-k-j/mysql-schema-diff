"""MySQL Schema Diff Reporter - Streamlit Application."""
import json
import os
import sys
from pathlib import Path
from typing import Dict, Optional, Tuple

# Add the parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from mysql.connector.errors import Error as MySQLError

from app.db import DatabaseConnection
from app.diff import compute_schema_diff, SchemaDiff
from app.render_markdown import build_markdown
from app.render_html import build_html

def init_session_state():
    """Initialize Streamlit session state variables."""
    if 'diff_result' not in st.session_state:
        st.session_state.diff_result = None
    if 'reviewed' not in st.session_state:
        st.session_state.reviewed = {}
    if 'compare_clicked' not in st.session_state:
        st.session_state.compare_clicked = False
    if 'saved_connection' not in st.session_state:
        st.session_state.saved_connection = False

def handle_connection(
    host: str,
    port: int,
    user: str,
    password: str,
    old_db: str,
    new_db: str
) -> Tuple[Optional[SchemaDiff], Optional[str]]:
    """Handle database connections and compute schema differences."""
    try:
        db = DatabaseConnection(host, port, user, password)
        
        # Fetch schemas
        old_tables = db.fetch_tables(old_db)
        new_tables = db.fetch_tables(new_db)
        
        old_columns = db.fetch_columns(old_db)
        new_columns = db.fetch_columns(new_db)
        
        # Compute differences
        diff = compute_schema_diff(old_tables, new_tables, old_columns, new_columns)
        
        # Initialize reviewed state for new tables
        tables_to_review = set()
        tables_to_review.update(diff.changed_tables.keys())
        tables_to_review.update(diff.added_tables)
        tables_to_review.update(diff.removed_tables)
        
        for table in tables_to_review:
            if table not in st.session_state.reviewed:
                st.session_state.reviewed[table] = False
        
        return diff, None
        
    except MySQLError as e:
        return None, f"Database error: {str(e)}"
    except Exception as e:
        return None, f"Error: {str(e)}"

def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="MySQL Schema Diff Reporter",
        page_icon="🔍",
        layout="wide"
    )
    
    st.title("MySQL Schema Diff Reporter")
    init_session_state()
    
    from app.utils import save_connection_details, load_connection_details, clear_connection_details

    # Sidebar inputs
    with st.sidebar:
        st.header("Database Connection")
        
        # Load saved connection details if available
        saved_details = load_connection_details()
        
        host = st.text_input("Host", 
                            value=saved_details.get('host', 'localhost') if saved_details else 'localhost')
        port = st.number_input("Port", 
                             value=saved_details.get('port', 3306) if saved_details else 3306,
                             min_value=1, max_value=65535)
        user = st.text_input("Username",
                            value=saved_details.get('username', '') if saved_details else '')
        password = st.text_input("Password", 
                               value=saved_details.get('password', '') if saved_details else '',
                               type="password")
        
        st.header("Databases")
        old_db = st.text_input("Old Database",
                              value=saved_details.get('old_db', '') if saved_details else '')
        new_db = st.text_input("New Database",
                              value=saved_details.get('new_db', '') if saved_details else '')
        
        # Add save/clear buttons in a two-column layout
        col1, col2 = st.columns(2)
        save_conn = col1.button("💾 Save Connection")
        clear_conn = col2.button("🗑️ Clear Saved")
        
        if save_conn:
            save_connection_details(host, port, user, password, old_db, new_db)
            st.success("Connection details saved!")
        
        if clear_conn:
            clear_connection_details()
            st.success("Saved connection details cleared!")
            st.rerun()
        
        st.divider()
        compare = st.button("🔍 Compare Schemas")
        
        if compare:
            st.session_state.compare_clicked = True
            with st.spinner("Comparing schemas..."):
                diff_result, error = handle_connection(
                    host, port, user, password, old_db, new_db
                )
                if error:
                    st.error(error)
                else:
                    st.session_state.diff_result = diff_result
    
    # Main content
    if st.session_state.compare_clicked:
        diff = st.session_state.diff_result
        if diff and diff.has_changes:
            # Summary
            st.header("Summary")
            cols = st.columns(3)
            if diff.added_tables:
                cols[0].metric("Added Tables", f"+{len(diff.added_tables)}")
            if diff.removed_tables:
                cols[1].metric("Removed Tables", f"-{len(diff.removed_tables)}")
            if diff.changed_tables:
                cols[2].metric("Changed Tables", len(diff.changed_tables))
            
            # Review controls
            st.header("Review Status")
            col1, col2 = st.columns(2)
            if col1.button("Check All"):
                for table in st.session_state.reviewed:
                    st.session_state.reviewed[table] = True
            if col2.button("Uncheck All"):
                for table in st.session_state.reviewed:
                    st.session_state.reviewed[table] = False
            
            # Added Tables
            if diff.added_tables:
                st.header("Added Tables")
                for table_name in sorted(diff.added_tables):
                    with st.expander(f"➕ {table_name}"):
                        st.checkbox(
                            "Reviewed",
                            key=f"reviewed_{table_name}",
                            value=st.session_state.reviewed.get(table_name, False),
                            on_change=lambda t=table_name: setattr(
                                st.session_state, 'reviewed',
                                {**st.session_state.reviewed, t: not st.session_state.reviewed[t]}
                            )
                        )
                        st.markdown(
                            "<span style='color: #16a34a'>✓ New table added to the schema</span>",
                            unsafe_allow_html=True
                        )

            # Removed Tables
            if diff.removed_tables:
                st.header("Removed Tables")
                for table_name in sorted(diff.removed_tables):
                    with st.expander(f"➖ {table_name}"):
                        st.checkbox(
                            "Reviewed",
                            key=f"reviewed_{table_name}",
                            value=st.session_state.reviewed.get(table_name, False),
                            on_change=lambda t=table_name: setattr(
                                st.session_state, 'reviewed',
                                {**st.session_state.reviewed, t: not st.session_state.reviewed[t]}
                            )
                        )
                        st.markdown(
                            "<span style='color: #dc2626'>✗ Table removed from the schema</span>",
                            unsafe_allow_html=True
                        )

            # Changed Tables
            if diff.changed_tables:
                st.header("Changed Tables")
                for table_name, table_diff in sorted(diff.changed_tables.items()):
                    with st.expander(f"📝 {table_name}"):
                        st.checkbox(
                            "Reviewed",
                            key=f"reviewed_{table_name}",
                            value=st.session_state.reviewed.get(table_name, False),
                            on_change=lambda t=table_name: setattr(
                                st.session_state, 'reviewed',
                                {**st.session_state.reviewed, t: not st.session_state.reviewed[t]}
                            )
                        )
                        
                        if table_diff.added_columns:
                            st.markdown("##### Added Columns")
                            for col_name, col_info in sorted(table_diff.added_columns.items()):
                                info_text = f"{col_name} ({col_info.column_type})"
                                if col_info.is_nullable == "NO":
                                    info_text += " NOT NULL"
                                if col_info.column_default:
                                    info_text += f" DEFAULT {col_info.column_default}"
                                if col_info.column_key:
                                    info_text += f" {col_info.column_key}"
                                st.markdown(
                                    f"<span style='color: #16a34a'>+ {info_text}</span>",
                                    unsafe_allow_html=True
                                )
                        
                        if table_diff.removed_columns:
                            st.markdown("##### Removed Columns")
                            for col_name, col_info in sorted(table_diff.removed_columns.items()):
                                info_text = f"{col_name} ({col_info.column_type})"
                                if col_info.is_nullable == "NO":
                                    info_text += " NOT NULL"
                                if col_info.column_default:
                                    info_text += f" DEFAULT {col_info.column_default}"
                                if col_info.column_key:
                                    info_text += f" {col_info.column_key}"
                                st.markdown(
                                    f"<span style='color: #dc2626'>- {info_text}</span>",
                                    unsafe_allow_html=True
                                )
            
            # Export buttons
            st.header("Export")
            col1, col2, col3 = st.columns(3)
            
            if col1.button("Export Markdown"):
                markdown = build_markdown(diff)
                st.download_button(
                    "Download Markdown",
                    markdown,
                    "schema_diff.md",
                    "text/markdown"
                )
            
            if col2.button("Export HTML"):
                html = build_html(diff, st.session_state.reviewed)
                st.download_button(
                    "Download HTML",
                    html,
                    "schema_diff.html",
                    "text/html"
                )
            
            if col3.button("Export Review Status"):
                reviewed_json = json.dumps(
                    st.session_state.reviewed,
                    indent=2
                )
                st.download_button(
                    "Download JSON",
                    reviewed_json,
                    "reviewed.json",
                    "application/json"
                )
        
        elif diff:
            st.info("No schema changes detected.")
    
if __name__ == "__main__":
    main()
