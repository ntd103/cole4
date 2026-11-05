#!/usr/bin/env python3
"""
HDFS Python Client Demo
Demonstrates basic HDFS operations using Python
"""

import os
import sys
from hdfs import InsecureClient
import pandas as pd
import json
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class HDFSManager:
    """A class to manage HDFS operations using Python"""
    
    def __init__(self, namenode_host='namenode', namenode_port=9870):
        """Initialize HDFS connection"""
        try:
            self.hdfs = InsecureClient(f'http://{namenode_host}:{namenode_port}')
            logger.info(f"Connected to HDFS at {namenode_host}:{namenode_port}")
        except Exception as e:
            logger.error(f"Failed to connect to HDFS: {e}")
            raise
    
    def list_directory(self, path='/'):
        """List contents of an HDFS directory"""
        try:
            contents = self.hdfs.list(path, status=True)
            logger.info(f"Listed {len(contents)} items in {path}")
            return contents
        except Exception as e:
            logger.error(f"Error listing directory {path}: {e}")
            return []
    
    def create_directory(self, path):
        """Create a directory in HDFS"""
        try:
            self.hdfs.makedirs(path)
            logger.info(f"Created directory: {path}")
            return True
        except Exception as e:
            logger.error(f"Error creating directory {path}: {e}")
            return False
    
    def upload_file(self, local_path, hdfs_path):
        """Upload a file from local filesystem to HDFS"""
        try:
            self.hdfs.upload(hdfs_path, local_path)
            logger.info(f"Uploaded {local_path} to {hdfs_path}")
            return True
        except Exception as e:
            logger.error(f"Error uploading file {local_path} to {hdfs_path}: {e}")
            return False
    
    def download_file(self, hdfs_path, local_path):
        """Download a file from HDFS to local filesystem"""
        try:
            self.hdfs.download(hdfs_path, local_path)
            logger.info(f"Downloaded {hdfs_path} to {local_path}")
            return True
        except Exception as e:
            logger.error(f"Error downloading file {hdfs_path} to {local_path}: {e}")
            return False
    
    def read_text_file(self, hdfs_path):
        """Read a text file from HDFS"""
        try:
            with self.hdfs.read(hdfs_path, encoding='utf-8') as reader:
                content = reader.read()
            logger.info(f"Read text file: {hdfs_path}")
            return content
        except Exception as e:
            logger.error(f"Error reading text file {hdfs_path}: {e}")
            return None
    
    def write_text_file(self, hdfs_path, content):
        """Write text content to HDFS"""
        try:
            with self.hdfs.write(hdfs_path, encoding='utf-8') as writer:
                writer.write(content)
            logger.info(f"Wrote text file: {hdfs_path}")
            return True
        except Exception as e:
            logger.error(f"Error writing text file {hdfs_path}: {e}")
            return False
    
    def delete_file(self, hdfs_path):
        """Delete a file or directory from HDFS"""
        try:
            self.hdfs.delete(hdfs_path, recursive=True)
            logger.info(f"Deleted: {hdfs_path}")
            return True
        except Exception as e:
            logger.error(f"Error deleting {hdfs_path}: {e}")
            return False
    
    def get_file_info(self, hdfs_path):
        """Get information about a file in HDFS"""
        try:
            info = self.hdfs.status(hdfs_path)
            logger.info(f"Got info for: {hdfs_path}")
            return info
        except Exception as e:
            logger.error(f"Error getting info for {hdfs_path}: {e}")
            return None

def demo_basic_operations():
    """Demonstrate basic HDFS operations"""
    print("=" * 50)
    print("HDFS Basic Operations Demo")
    print("=" * 50)
    
    # Initialize HDFS manager
    hdfs_manager = HDFSManager()
    
    # 1. Create directories
    print("\n1. Creating directories...")
    hdfs_manager.create_directory('/demo')
    hdfs_manager.create_directory('/demo/data')
    hdfs_manager.create_directory('/demo/output')
    
    # 2. List root directory
    print("\n2. Listing root directory...")
    contents = hdfs_manager.list_directory('/')
    for item in contents:
        item_type = "Directory" if item[1]['type'] == 'DIRECTORY' else "File"
        print(f"  {item[0]} - Size: {item[1]['length']} bytes - Type: {item_type}")
    
    # 3. Create and upload a sample file
    print("\n3. Creating and uploading sample data...")
    sample_data = {
        'students': [
            {'name': 'Alice', 'age': 22, 'grade': 'A'},
            {'name': 'Bob', 'age': 23, 'grade': 'B'},
            {'name': 'Charlie', 'age': 21, 'grade': 'A'},
            {'name': 'Diana', 'age': 24, 'grade': 'B+'}
        ],
        'timestamp': datetime.now().isoformat()
    }
    
    # Write JSON data
    json_content = json.dumps(sample_data, indent=2)
    hdfs_manager.write_text_file('/demo/data/students.json', json_content)
    
    # Write CSV data
    df = pd.DataFrame(sample_data['students'])
    csv_content = df.to_csv(index=False)
    hdfs_manager.write_text_file('/demo/data/students.csv', csv_content)
    
    # 4. Read and display file content
    print("\n4. Reading file content...")
    json_content = hdfs_manager.read_text_file('/demo/data/students.json')
    print("JSON Content:")
    print(json_content)
    
    # 5. Get file information
    print("\n5. File information...")
    info = hdfs_manager.get_file_info('/demo/data/students.json')
    if info:
        print(f"  File: students.json")
        print(f"  Size: {info['length']} bytes")
        print(f"  Replication: {info['replication']}")
        print(f"  Block size: {info['blockSize']} bytes")

def demo_data_processing():
    """Demonstrate data processing with HDFS"""
    print("\n" + "=" * 50)
    print("HDFS Data Processing Demo")
    print("=" * 50)
    
    hdfs_manager = HDFSManager()
    
    # Generate sample sales data
    print("\n1. Generating sample sales data...")
    import random
    
    sales_data = []
    products = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones']
    regions = ['North', 'South', 'East', 'West']
    
    for i in range(100):
        sale = {
            'id': i + 1,
            'product': random.choice(products),
            'region': random.choice(regions),
            'sales_amount': round(random.uniform(100, 2000), 2),
            'date': f"2023-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
        }
        sales_data.append(sale)
    
    # Save to HDFS
    df_sales = pd.DataFrame(sales_data)
    csv_content = df_sales.to_csv(index=False)
    hdfs_manager.write_text_file('/demo/data/sales_data.csv', csv_content)
    
    # Process data
    print("\n2. Processing sales data...")
    
    # Read data back from HDFS
    csv_content = hdfs_manager.read_text_file('/demo/data/sales_data.csv')
    
    # Create DataFrame from CSV content
    from io import StringIO
    df = pd.read_csv(StringIO(csv_content))
    
    # Perform analysis
    print(f"Total records: {len(df)}")
    print(f"Total sales: ${df['sales_amount'].sum():,.2f}")
    print(f"Average sales: ${df['sales_amount'].mean():.2f}")
    
    # Group by product
    product_sales = df.groupby('product')['sales_amount'].agg(['sum', 'mean', 'count'])
    print("\nSales by Product:")
    print(product_sales)
    
    # Group by region
    region_sales = df.groupby('region')['sales_amount'].agg(['sum', 'mean', 'count'])
    print("\nSales by Region:")
    print(region_sales)
    
    # Save processed results
    print("\n3. Saving processed results...")
    
    # Save product analysis
    product_analysis = product_sales.to_csv()
    hdfs_manager.write_text_file('/demo/output/product_analysis.csv', product_analysis)
    
    # Save region analysis
    region_analysis = region_sales.to_csv()
    hdfs_manager.write_text_file('/demo/output/region_analysis.csv', region_analysis)
    
    # Save summary report
    summary_report = f"""
Sales Data Analysis Report
Generated: {datetime.now().isoformat()}

Summary Statistics:
- Total Records: {len(df)}
- Total Sales: ${df['sales_amount'].sum():,.2f}
- Average Sales: ${df['sales_amount'].mean():.2f}
- Min Sales: ${df['sales_amount'].min():.2f}
- Max Sales: ${df['sales_amount'].max():.2f}

Top Product by Sales: {product_sales['sum'].idxmax()}
Top Region by Sales: {region_sales['sum'].idxmax()}
"""
    hdfs_manager.write_text_file('/demo/output/summary_report.txt', summary_report)
    
    print("Analysis complete! Results saved to /demo/output/")

if __name__ == "__main__":
    try:
        demo_basic_operations()
        demo_data_processing()
        print("\n" + "=" * 50)
        print("Demo completed successfully!")
        print("=" * 50)
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        sys.exit(1)
