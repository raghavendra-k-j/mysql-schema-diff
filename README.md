# MySQL Schema Diff Reporter

A tool to compare MySQL database schemas and generate diff reports in Markdown and HTML formats.

## Features

- Compare two MySQL database schemas
- Detect added and removed tables
- Detect added and removed columns in existing tables
- Generate Markdown and HTML reports
- Interactive Streamlit UI with review checkboxes
- Export review status as JSON

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd mysql-schema-diff
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate # Linux/macOS
   ```

3. Install dependencies and the package:
   ```bash
   pip install -r requirements.txt
   pip install -e .  # Install the package in development mode
   ```

## Usage

1. Start the application:
   ```bash
   python run.py
   ```

2. In the sidebar:
   - Enter MySQL connection details (host, port, username, password)
   - Specify the old and new database names
   - Click "Compare Schemas"

3. Review the differences:
   - View added/removed tables and column changes
   - Use checkboxes to mark reviewed items
   - Use "Check All" / "Uncheck All" buttons for bulk actions

4. Export reports:
   - Click "Export Markdown" for a text-based report
   - Click "Export HTML" for a styled report with checkboxes
   - Click "Export Review Status" to save review progress as JSON

## Output Files

- `schema_diff.md`: Markdown report with all changes
- `schema_diff.html`: HTML report with styling and checkboxes
- `reviewed.json`: JSON file with review status of each table

## Security Notes

- Database credentials are not logged or stored
- Read-only operations only; no database modifications
- Local file output only; no network transmission of data

## Requirements

- Python 3.10 or higher
- MySQL Server
- Required Python packages (see requirements.txt):
  - streamlit
  - mysql-connector-python
  - pandas
  - jinja2
