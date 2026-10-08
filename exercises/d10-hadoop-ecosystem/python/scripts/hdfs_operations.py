#!/usr/bin/env python3
"""
HDFS Operations with Python
This script demonstrates how to interact with HDFS using Python
"""

from hdfs3 import HDFileSystem
import pandas as pd
import json
import os

class HDFSManager:
    def __init__(self, namenode_host='namenode', namenode_port=9000):
        """Initialize HDFS connection"""
        self.hdfs = HDFileSystem(host=namenode_host, port=namenode_port)
        
    def list_directory(self, path='/'):
        """List contents of HDFS directory"""
        try:
            return self.hdfs.ls(path)
        except Exception as e:
            print(f"Error listing directory {path}: {e}")
            return []
    
    def create_directory(self, path):
        """Create directory in HDFS"""
        try:
            self.hdfs.mkdir(path)
            print(f"Directory created: {path}")
        except Exception as e:
            print(f"Error creating directory {path}: {e}")
    
    def upload_file(self, local_path, hdfs_path):
        """Upload file from local system to HDFS"""
        try:
            self.hdfs.put(local_path, hdfs_path)
            print(f"File uploaded: {local_path} -> {hdfs_path}")
        except Exception as e:
            print(f"Error uploading file: {e}")
    
    def download_file(self, hdfs_path, local_path):
        """Download file from HDFS to local system"""
        try:
            self.hdfs.get(hdfs_path, local_path)
            print(f"File downloaded: {hdfs_path} -> {local_path}")
        except Exception as e:
            print(f"Error downloading file: {e}")
    
    def read_csv_from_hdfs(self, hdfs_path):
        """Read CSV file directly from HDFS into pandas DataFrame"""
        try:
            with self.hdfs.open(hdfs_path, 'rb') as f:
                df = pd.read_csv(f)
            return df
        except Exception as e:
            print(f"Error reading CSV from HDFS: {e}")
            return None
    
    def write_csv_to_hdfs(self, df, hdfs_path):
        """Write pandas DataFrame to CSV in HDFS"""
        try:
            with self.hdfs.open(hdfs_path, 'wb') as f:
                df.to_csv(f, index=False)
            print(f"CSV written to HDFS: {hdfs_path}")
        except Exception as e:
            print(f"Error writing CSV to HDFS: {e}")
    
    def get_file_info(self, hdfs_path):
        """Get information about a file in HDFS"""
        try:
            return self.hdfs.info(hdfs_path)
        except Exception as e:
            print(f"Error getting file info: {e}")
            return None

def main():
    """Main function demonstrating HDFS operations"""
    # Initialize HDFS manager
    hdfs_manager = HDFSManager()
    
    # Create directories
    print("Creating HDFS directories...")
    hdfs_manager.create_directory('/user/python')
    hdfs_manager.create_directory('/user/python/input')
    hdfs_manager.create_directory('/user/python/output')
    
    # List root directory
    print("\nListing HDFS root directory:")
    root_contents = hdfs_manager.list_directory('/')
    for item in root_contents:
        print(f"  {item}")
    
    # Upload sample data files
    print("\nUploading sample data files...")
    data_files = [
        ('/data/employees.csv', '/user/python/input/employees.csv'),
        ('/data/sales.csv', '/user/python/input/sales.csv'),
        ('/data/customers.json', '/user/python/input/customers.json')
    ]
    
    for local_path, hdfs_path in data_files:
        if os.path.exists(local_path):
            hdfs_manager.upload_file(local_path, hdfs_path)
    
    # Read and process data
    print("\nReading and processing data from HDFS...")
    employees_df = hdfs_manager.read_csv_from_hdfs('/user/python/input/employees.csv')
    if employees_df is not None:
        print(f"Employees data shape: {employees_df.shape}")
        print(employees_df.head())
        
        # Process data - calculate department statistics
        dept_stats = employees_df.groupby('department').agg({
            'salary': ['count', 'mean', 'max', 'min'],
            'employee_id': 'count'
        }).round(2)
        dept_stats.columns = ['employee_count', 'avg_salary', 'max_salary', 'min_salary', 'total_employees']
        
        # Write processed data back to HDFS
        hdfs_manager.write_csv_to_hdfs(dept_stats, '/user/python/output/department_statistics.csv')
    
    # Get file information
    print("\nFile information:")
    for _, hdfs_path in data_files:
        info = hdfs_manager.get_file_info(hdfs_path)
        if info:
            print(f"{hdfs_path}: {info['size']} bytes")

if __name__ == "__main__":
    main()
