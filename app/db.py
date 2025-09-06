"""Database connection and schema introspection module."""
from typing import Dict, Set, Optional, NamedTuple
import mysql.connector
from mysql.connector.errors import Error as MySQLError

class ColumnInfo(NamedTuple):
    """Column information from information_schema."""
    name: str
    data_type: str
    column_type: str
    is_nullable: str
    column_default: Optional[str]
    column_key: str
    extra: str

class DatabaseConnection:
    """Handles MySQL database connections and schema introspection."""
    
    def __init__(self, host: str, port: int, user: str, password: str):
        """Initialize database connection parameters."""
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self._conn = None

    def connect(self, database: str) -> None:
        """Establish connection to the MySQL database."""
        try:
            self._conn = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=database
            )
        except MySQLError as e:
            raise ConnectionError(f"Failed to connect to database: {e}")

    def close(self) -> None:
        """Close the database connection."""
        if self._conn:
            self._conn.close()

    def fetch_tables(self, database: str) -> Set[str]:
        """Fetch all table names from the given database."""
        self.connect(database)
        try:
            cursor = self._conn.cursor()
            cursor.execute("""
                SELECT TABLE_NAME 
                FROM information_schema.TABLES 
                WHERE TABLE_SCHEMA = %s 
                AND TABLE_TYPE = 'BASE TABLE'
            """, (database,))
            return {row[0] for row in cursor.fetchall()}
        finally:
            self.close()

    def fetch_columns(self, database: str) -> Dict[str, Dict[str, ColumnInfo]]:
        """Fetch all column information for all tables in the database."""
        self.connect(database)
        try:
            cursor = self._conn.cursor()
            cursor.execute("""
                SELECT 
                    TABLE_NAME,
                    COLUMN_NAME,
                    DATA_TYPE,
                    COLUMN_TYPE,
                    IS_NULLABLE,
                    COLUMN_DEFAULT,
                    COLUMN_KEY,
                    EXTRA
                FROM information_schema.COLUMNS 
                WHERE TABLE_SCHEMA = %s
                ORDER BY TABLE_NAME, ORDINAL_POSITION
            """, (database,))
            
            columns: Dict[str, Dict[str, ColumnInfo]] = {}
            for row in cursor.fetchall():
                table_name = row[0]
                if table_name not in columns:
                    columns[table_name] = {}
                
                columns[table_name][row[1]] = ColumnInfo(
                    name=row[1],
                    data_type=row[2],
                    column_type=row[3],
                    is_nullable=row[4],
                    column_default=row[5],
                    column_key=row[6],
                    extra=row[7]
                )
            return columns
        finally:
            self.close()
