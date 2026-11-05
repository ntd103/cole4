#!/usr/bin/env python3
"""
Exercise 1: Basic HDFS Operations
Level: Beginner

Learning Objectives:
- Connect to HDFS using Python
- Create directories in HDFS
- Upload and download files
- List directory contents
- Get file information

Tasks:
1. Connect to the HDFS cluster
2. Create a directory structure /exercises/exercise1/
3. Upload the sample_employees.csv file to HDFS
4. List the contents of your directory
5. Download the file back to a different location
6. Display file information (size, replication factor, etc.)
"""

from hdfs import InsecureClient
import os

def exercise1():
    """Complete the basic HDFS operations"""
    
    # TODO: Task 1 - Connect to HDFS
    # Initialize HDFileSystem with namenode host and port
    hdfs = None  # Replace with your connection
    
    # TODO: Task 2 - Create directory structure
    # Create /exercises/exercise1/ directory
    
    # TODO: Task 3 - Upload file
    # Upload /data/sample_employees.csv to /exercises/exercise1/employees.csv
    
    # TODO: Task 4 - List directory contents
    # List and print the contents of /exercises/exercise1/
    
    # TODO: Task 5 - Download file
    # Download the file to /exercises/downloaded_employees.csv
    
    # TODO: Task 6 - Display file information
    # Get and print file information for the uploaded file
    
    print("Exercise 1 completed!")

if __name__ == "__main__":
    exercise1()

# Expected Output:
"""
Directory created: /exercises/exercise1/
File uploaded successfully
Directory contents:
  /exercises/exercise1/employees.csv - Size: XXX bytes
File downloaded successfully
File Info:
  Name: /exercises/exercise1/employees.csv
  Size: XXX bytes
  Replication: 2
  Block size: XXXXXXX bytes
Exercise 1 completed!
"""

# Hints:
"""
1. Use InsecureClient('http://namenode:9870') to connect
2. Use hdfs.makedirs(path) to create directories
3. Use hdfs.upload(hdfs_path, local_path) for uploads
4. Use hdfs.list(path, status=True) to list contents
5. Use hdfs.download(hdfs_path, local_path) for downloads
6. Use hdfs.status(path) to get file information
"""
