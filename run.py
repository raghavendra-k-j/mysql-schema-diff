"""Launcher for MySQL Schema Diff Reporter."""
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

if __name__ == "__main__":
    # Get the absolute path to main.py
    app_path = str(project_root / "app" / "main.py")
    
    # Use os.system to run streamlit directly
    os.system(f'streamlit run "{app_path}"')
