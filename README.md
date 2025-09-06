# MySQL Schema Diff Reporter

A powerful tool for comparing MySQL database schemas and generating detailed, interactive diff reports. Perfect for database migrations, schema reviews, and change tracking.

![MySQL Schema Diff Reporter](https://raw.githubusercontent.com/raghavendra-k-j/mysql-schema-diff/main/docs/images/preview.png)

## 🌟 Features

### Core Functionality
- **Schema Comparison**: Compare two MySQL databases and identify all structural differences
- **Detailed Analysis**: Track changes in tables and columns with precise type information
- **Read-Only Operations**: Safe, non-destructive database access

### Change Detection
- ➕ Added tables and their complete structure
- ➖ Removed tables and their previous structure
- 📝 Modified tables with column-level changes:
  - New columns added
  - Columns removed
  - Full column details (type, nullability, defaults, keys)

### Interactive UI
- **Modern Interface**: Clean, responsive Streamlit-based UI
- **Connection Management**:
  - 💾 Save connection details securely
  - 🔐 Encrypted password storage
  - 🗑️ Clear saved credentials option
- **Review Workflow**:
  - ✓ Checkbox-based review tracking
  - 📊 Progress indicators
  - Bulk actions (Check All/Uncheck All)

### Export Options
- 📄 **Markdown Report** (`schema_diff.md`):
  - Clean, readable format
  - Perfect for version control
  - Sections for added, removed, and modified tables
  
- 🎨 **HTML Report** (`schema_diff.html`):
  - Professional styling with Git-style diffs
  - Green/Red color coding for additions/removals
  - Interactive table of contents
  - Review checkboxes
  - Mobile-responsive design
  
- 📋 **Review Status** (`reviewed.json`):
  - Track review progress
  - Export review state for documentation

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- MySQL Server
- Git

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/raghavendra-k-j/mysql-schema-diff.git
   cd mysql-schema-diff
   ```

2. **Set Up Python Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate it:
   # On Windows:
   .\venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -e .  # Install package in development mode
   ```

### Running the Application

1. **Start the App**
   ```bash
   python run.py
   ```

2. **Configure Connection**
   - Enter MySQL connection details:
     - Host (default: localhost)
     - Port (default: 3306)
     - Username
     - Password
     - Old database name
     - New database name
   - Optionally save connection details for future use

3. **Compare Schemas**
   - Click "🔍 Compare Schemas"
   - Review the differences in three sections:
     - Added Tables (green)
     - Removed Tables (red)
     - Changed Tables (with column details)

4. **Review Changes**
   - Expand/collapse table sections
   - Check/uncheck tables as you review
   - Use bulk actions for efficient review

5. **Export Reports**
   - Generate Markdown report
   - Generate HTML report
   - Export review status

## 🔒 Security Features

- **Secure Storage**:
  - Connection details stored locally
  - Passwords encrypted using industry-standard cryptography
  - No remote data transmission

- **Safe Operations**:
  - Read-only database access
  - No schema modifications
  - No data access beyond schema metadata

## 🛠️ Technical Details

### Dependencies
- **Core**:
  - `streamlit>=1.26.0`: Modern web UI
  - `mysql-connector-python>=8.1.0`: Database connectivity
  - `jinja2>=3.1.2`: HTML report templating
  - `cryptography>=41.0.0`: Secure credential storage

### Database Access
- Uses `information_schema` for metadata
- Key queries:
  ```sql
  -- Tables
  SELECT TABLE_NAME FROM information_schema.TABLES 
  WHERE TABLE_SCHEMA = %s AND TABLE_TYPE = 'BASE TABLE'

  -- Columns
  SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE, ...
  FROM information_schema.COLUMNS 
  WHERE TABLE_SCHEMA = %s
  ```

### Project Structure
```
mysql-schema-diff/
├── app/
│   ├── __init__.py
│   ├── main.py          # Streamlit UI
│   ├── db.py            # Database operations
│   ├── diff.py          # Schema comparison
│   ├── render_markdown.py
│   ├── render_html.py
│   ├── utils.py         # Helper functions
│   └── templates/
│       └── report.html.j2
├── requirements.txt
├── setup.py
└── README.md
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Inspired by the need for better database schema comparison tools
- Built with Python and modern web technologies
- Special thanks to the Streamlit team for their amazing framework
