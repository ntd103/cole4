"""
ClickHouse database connection and utility functions.
"""
import os
import clickhouse_connect
from typing import Optional, Dict, Any, List
import pandas as pd
from rich.console import Console

console = Console()

class ClickHouseManager:
    """Manages ClickHouse database connections and operations."""
    
    def __init__(self):
        self.host = os.getenv('CLICKHOUSE_HOST', 'localhost')
        self.port = int(os.getenv('CLICKHOUSE_PORT', '8123'))
        self.user = os.getenv('CLICKHOUSE_USER', 'admin')
        self.password = os.getenv('CLICKHOUSE_PASSWORD', 'admin123')
        self.client = None
        self._connect()
    
    def _connect(self):
        """Establish connection to ClickHouse."""
        try:
            self.client = clickhouse_connect.get_client(
                host=self.host,
                port=self.port,
                username=self.user,
                password=self.password
            )
            console.print(f"✓ Connected to ClickHouse at {self.host}:{self.port}")
        except Exception as e:
            console.print(f"✗ Failed to connect to ClickHouse: {e}")
            raise
    
    def test_connection(self) -> bool:
        """Test the database connection."""
        try:
            result = self.client.query("SELECT 1")
            return True
        except Exception as e:
            console.print(f"Connection test failed: {e}")
            return False
    
    def execute_query(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> Any:
        """Execute a query and return results."""
        try:
            if parameters:
                return self.client.query(query, parameters=parameters)
            else:
                return self.client.query(query)
        except Exception as e:
            console.print(f"Query execution failed: {e}")
            console.print(f"Query: {query}")
            raise
    
    def execute_insert(self, table: str, data: List[Dict[str, Any]], database: str = None):
        """Insert data into a table."""
        try:
            full_table = f"{database}.{table}" if database else table
            self.client.insert(full_table, data)
            console.print(f"✓ Inserted {len(data)} rows into {full_table}")
        except Exception as e:
            console.print(f"Insert failed: {e}")
            raise
    
    def query_to_dataframe(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """Execute query and return results as pandas DataFrame."""
        try:
            result = self.execute_query(query, parameters)
            return result.result_set.to_pandas()
        except Exception as e:
            console.print(f"DataFrame query failed: {e}")
            raise
    
    def get_table_count(self, database: str) -> int:
        """Get number of tables in a database."""
        query = f"SELECT count() FROM system.tables WHERE database = '{database}'"
        result = self.execute_query(query)
        return result.result_rows[0][0] if result.result_rows else 0
    
    def get_row_count(self, database: str) -> int:
        """Get total row count across all tables in a database."""
        query = f"""
        SELECT sum(total_rows) 
        FROM system.tables 
        WHERE database = '{database}' AND engine NOT LIKE '%View%'
        """
        result = self.execute_query(query)
        return result.result_rows[0][0] if result.result_rows and result.result_rows[0][0] else 0
    
    def get_database_size(self, database: str) -> float:
        """Get database size in MB."""
        query = f"""
        SELECT sum(total_bytes) / 1024 / 1024 as size_mb
        FROM system.tables 
        WHERE database = '{database}' AND engine NOT LIKE '%View%'
        """
        result = self.execute_query(query)
        return result.result_rows[0][0] if result.result_rows and result.result_rows[0][0] else 0.0
    
    def drop_database_if_exists(self, database: str):
        """Drop database if it exists."""
        query = f"DROP DATABASE IF EXISTS {database}"
        self.execute_query(query)
        console.print(f"✓ Dropped database {database}")
    
    def create_database_if_not_exists(self, database: str):
        """Create database if it doesn't exist."""
        query = f"CREATE DATABASE IF NOT EXISTS {database}"
        self.execute_query(query)
        console.print(f"✓ Created database {database}")
    
    def get_table_schema(self, database: str, table: str) -> pd.DataFrame:
        """Get table schema information."""
        query = f"""
        SELECT 
            name,
            type,
            default_kind,
            default_expression,
            comment
        FROM system.columns 
        WHERE database = '{database}' AND table = '{table}'
        ORDER BY position
        """
        return self.query_to_dataframe(query)
    
    def execute_script_file(self, file_path: str):
        """Execute SQL script from file."""
        try:
            with open(file_path, 'r') as f:
                script = f.read()
            
            # Split by semicolon and execute each statement
            statements = [stmt.strip() for stmt in script.split(';') if stmt.strip()]
            
            for stmt in statements:
                if stmt:
                    self.execute_query(stmt)
            
            console.print(f"✓ Executed script: {file_path}")
        except Exception as e:
            console.print(f"Script execution failed: {e}")
            raise
    
    def close(self):
        """Close the database connection."""
        if self.client:
            self.client.close()
            console.print("✓ Database connection closed")
