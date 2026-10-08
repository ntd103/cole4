#!/usr/bin/env python3
"""
HBase Operations with Python
This script demonstrates how to interact with HBase using Python
"""

import happybase
import json
from datetime import datetime

class HBaseManager:
    def __init__(self, host='hbase-master', port=9090):
        """Initialize HBase connection"""
        try:
            self.connection = happybase.Connection(host=host, port=port)
            print(f"Connected to HBase at {host}:{port}")
        except Exception as e:
            print(f"Error connecting to HBase: {e}")
            self.connection = None
    
    def list_tables(self):
        """List all tables in HBase"""
        if self.connection:
            try:
                tables = self.connection.tables()
                return [table.decode('utf-8') for table in tables]
            except Exception as e:
                print(f"Error listing tables: {e}")
                return []
        return []
    
    def create_table(self, table_name, column_families):
        """Create a new table with specified column families"""
        if self.connection:
            try:
                families = {cf: dict() for cf in column_families}
                self.connection.create_table(table_name, families)
                print(f"Table '{table_name}' created successfully")
            except Exception as e:
                print(f"Error creating table '{table_name}': {e}")
    
    def insert_data(self, table_name, row_key, data):
        """Insert data into HBase table"""
        if self.connection:
            try:
                table = self.connection.table(table_name)
                table.put(row_key, data)
                print(f"Data inserted into '{table_name}' with key '{row_key}'")
            except Exception as e:
                print(f"Error inserting data: {e}")
    
    def get_row(self, table_name, row_key):
        """Get a specific row from HBase table"""
        if self.connection:
            try:
                table = self.connection.table(table_name)
                return table.row(row_key)
            except Exception as e:
                print(f"Error getting row: {e}")
                return None
        return None
    
    def scan_table(self, table_name, limit=10):
        """Scan HBase table and return rows"""
        if self.connection:
            try:
                table = self.connection.table(table_name)
                rows = []
                for key, data in table.scan(limit=limit):
                    rows.append((key.decode('utf-8'), {k.decode('utf-8'): v.decode('utf-8') for k, v in data.items()}))
                return rows
            except Exception as e:
                print(f"Error scanning table: {e}")
                return []
        return []
    
    def delete_row(self, table_name, row_key):
        """Delete a row from HBase table"""
        if self.connection:
            try:
                table = self.connection.table(table_name)
                table.delete(row_key)
                print(f"Row '{row_key}' deleted from '{table_name}'")
            except Exception as e:
                print(f"Error deleting row: {e}")
    
    def close_connection(self):
        """Close HBase connection"""
        if self.connection:
            self.connection.close()
            print("HBase connection closed")

def load_sample_data(hbase_manager):
    """Load sample data into HBase tables"""
    
    # Create employee profiles table
    hbase_manager.create_table('employee_profiles_python', ['personal', 'professional', 'contact'])
    
    # Sample employee data
    employees = [
        {
            'row_key': '1001',
            'data': {
                'personal:first_name': 'John',
                'personal:last_name': 'Smith',
                'professional:department': 'Engineering',
                'professional:salary': '75000',
                'professional:hire_date': '2020-01-15',
                'contact:email': 'john.smith@company.com'
            }
        },
        {
            'row_key': '1002',
            'data': {
                'personal:first_name': 'Jane',
                'personal:last_name': 'Doe',
                'professional:department': 'Marketing',
                'professional:salary': '65000',
                'professional:hire_date': '2020-02-20',
                'contact:email': 'jane.doe@company.com'
            }
        }
    ]
    
    # Insert employee data
    for emp in employees:
        hbase_manager.insert_data('employee_profiles_python', emp['row_key'], emp['data'])
    
    # Create sales analytics table
    hbase_manager.create_table('sales_analytics_python', ['transaction', 'metrics'])
    
    # Sample sales analytics data
    sales_data = [
        {
            'row_key': 'daily_2024_01_15',
            'data': {
                'transaction:total_sales': '5',
                'transaction:total_revenue': '3275.00',
                'metrics:avg_order_value': '655.00',
                'metrics:top_product': 'Laptop'
            }
        },
        {
            'row_key': 'daily_2024_01_16',
            'data': {
                'transaction:total_sales': '3',
                'transaction:total_revenue': '1850.00',
                'metrics:avg_order_value': '616.67',
                'metrics:top_product': 'Monitor'
            }
        }
    ]
    
    # Insert sales analytics data
    for sale in sales_data:
        hbase_manager.insert_data('sales_analytics_python', sale['row_key'], sale['data'])

def main():
    """Main function demonstrating HBase operations"""
    # Initialize HBase manager
    hbase_manager = HBaseManager()
    
    if not hbase_manager.connection:
        print("Could not connect to HBase. Exiting.")
        return
    
    try:
        # List existing tables
        print("Existing HBase tables:")
        tables = hbase_manager.list_tables()
        for table in tables:
            print(f"  {table}")
        
        # Load sample data
        print("\nLoading sample data...")
        load_sample_data(hbase_manager)
        
        # Query data
        print("\nQuerying employee data:")
        employee_row = hbase_manager.get_row('employee_profiles_python', '1001')
        if employee_row:
            print("Employee 1001:")
            for col, value in employee_row.items():
                print(f"  {col.decode('utf-8')}: {value.decode('utf-8')}")
        
        # Scan tables
        print("\nScanning employee profiles:")
        employee_rows = hbase_manager.scan_table('employee_profiles_python')
        for row_key, data in employee_rows:
            print(f"Row Key: {row_key}")
            for col, value in data.items():
                print(f"  {col}: {value}")
            print()
        
        print("Scanning sales analytics:")
        sales_rows = hbase_manager.scan_table('sales_analytics_python')
        for row_key, data in sales_rows:
            print(f"Row Key: {row_key}")
            for col, value in data.items():
                print(f"  {col}: {value}")
            print()
        
        # Update data
        print("Updating employee salary...")
        hbase_manager.insert_data('employee_profiles_python', '1001', 
                                 {'professional:salary': '80000'})
        
        # Verify update
        updated_row = hbase_manager.get_row('employee_profiles_python', '1001')
        if updated_row and b'professional:salary' in updated_row:
            new_salary = updated_row[b'professional:salary'].decode('utf-8')
            print(f"Updated salary for employee 1001: {new_salary}")
        
    finally:
        # Close connection
        hbase_manager.close_connection()

if __name__ == "__main__":
    main()
