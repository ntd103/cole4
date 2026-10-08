#!/usr/bin/env python3
"""
PySpark Data Processing with Hadoop Integration
This script demonstrates big data processing using PySpark with Hadoop ecosystem
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as spark_sum, avg, max as spark_max, min as spark_min, count
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, DateType
import pandas as pd

class SparkHadoopProcessor:
    def __init__(self, app_name="HadoopEcosystemDemo"):
        """Initialize Spark session with Hadoop configuration"""
        self.spark = SparkSession.builder \
            .appName(app_name) \
            .config("spark.sql.adaptive.enabled", "true") \
            .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
            .getOrCreate()
        
        # Set log level to reduce verbosity
        self.spark.sparkContext.setLogLevel("WARN")
        print(f"Spark session initialized: {app_name}")
    
    def read_csv_from_hdfs(self, hdfs_path, header=True, infer_schema=True):
        """Read CSV file from HDFS into Spark DataFrame"""
        try:
            df = self.spark.read \
                .option("header", header) \
                .option("inferSchema", infer_schema) \
                .csv(hdfs_path)
            print(f"Read CSV from HDFS: {hdfs_path}")
            return df
        except Exception as e:
            print(f"Error reading CSV from HDFS: {e}")
            return None
    
    def write_csv_to_hdfs(self, df, hdfs_path, mode="overwrite"):
        """Write Spark DataFrame to CSV in HDFS"""
        try:
            df.coalesce(1).write \
                .mode(mode) \
                .option("header", "true") \
                .csv(hdfs_path)
            print(f"Written CSV to HDFS: {hdfs_path}")
        except Exception as e:
            print(f"Error writing CSV to HDFS: {e}")
    
    def read_parquet_from_hdfs(self, hdfs_path):
        """Read Parquet file from HDFS into Spark DataFrame"""
        try:
            df = self.spark.read.parquet(hdfs_path)
            print(f"Read Parquet from HDFS: {hdfs_path}")
            return df
        except Exception as e:
            print(f"Error reading Parquet from HDFS: {e}")
            return None
    
    def write_parquet_to_hdfs(self, df, hdfs_path, mode="overwrite"):
        """Write Spark DataFrame to Parquet in HDFS"""
        try:
            df.write \
                .mode(mode) \
                .parquet(hdfs_path)
            print(f"Written Parquet to HDFS: {hdfs_path}")
        except Exception as e:
            print(f"Error writing Parquet to HDFS: {e}")
    
    def analyze_employees(self, employees_df):
        """Analyze employee data"""
        print("\n=== Employee Analysis ===")
        
        # Show basic statistics
        print("Employee count by department:")
        dept_count = employees_df.groupBy("department").count().orderBy("count", ascending=False)
        dept_count.show()
        
        # Salary statistics by department
        print("Salary statistics by department:")
        salary_stats = employees_df.groupBy("department").agg(
            count("employee_id").alias("employee_count"),
            avg("salary").alias("avg_salary"),
            spark_max("salary").alias("max_salary"),
            spark_min("salary").alias("min_salary")
        ).orderBy("avg_salary", ascending=False)
        salary_stats.show()
        
        return salary_stats
    
    def analyze_sales(self, sales_df):
        """Analyze sales data"""
        print("\n=== Sales Analysis ===")
        
        # Sales by region
        print("Sales by region:")
        region_sales = sales_df.groupBy("region").agg(
            count("sale_id").alias("total_sales"),
            spark_sum(col("quantity") * col("unit_price")).alias("total_revenue"),
            avg(col("quantity") * col("unit_price")).alias("avg_order_value")
        ).orderBy("total_revenue", ascending=False)
        region_sales.show()
        
        # Top selling products
        print("Top selling products:")
        product_sales = sales_df.groupBy("product_name").agg(
            spark_sum("quantity").alias("total_quantity"),
            spark_sum(col("quantity") * col("unit_price")).alias("total_revenue"),
            count("sale_id").alias("num_orders")
        ).orderBy("total_revenue", ascending=False)
        product_sales.show()
        
        return region_sales, product_sales
    
    def join_employee_sales(self, employees_df, sales_df):
        """Join employee and sales data for analysis"""
        print("\n=== Employee Sales Performance ===")
        
        # Join employees with their sales
        employee_sales = employees_df.alias("e").join(
            sales_df.alias("s"),
            col("e.employee_id") == col("s.employee_id"),
            "left"
        )
        
        # Calculate sales performance by employee
        performance = employee_sales.groupBy(
            "e.employee_id", "e.first_name", "e.last_name", "e.department"
        ).agg(
            count("s.sale_id").alias("total_sales"),
            spark_sum(col("s.quantity") * col("s.unit_price")).alias("total_revenue")
        ).fillna(0).orderBy("total_revenue", ascending=False)
        
        print("Employee sales performance:")
        performance.show()
        
        return performance
    
    def create_data_mart(self, employees_df, sales_df):
        """Create a data mart combining multiple datasets"""
        print("\n=== Creating Data Mart ===")
        
        # Department performance summary
        dept_performance = employees_df.alias("e").join(
            sales_df.alias("s"),
            col("e.employee_id") == col("s.employee_id"),
            "left"
        ).groupBy("e.department").agg(
            count("e.employee_id").alias("employee_count"),
            avg("e.salary").alias("avg_salary"),
            count("s.sale_id").alias("total_sales"),
            spark_sum(col("s.quantity") * col("s.unit_price")).alias("total_revenue")
        ).fillna(0)
        
        print("Department performance data mart:")
        dept_performance.show()
        
        return dept_performance
    
    def stop_session(self):
        """Stop Spark session"""
        self.spark.stop()
        print("Spark session stopped")

def main():
    """Main function demonstrating PySpark with Hadoop"""
    # Initialize Spark processor
    processor = SparkHadoopProcessor()
    
    try:
        # Read data from HDFS (simulating with local files for demo)
        print("Reading data from HDFS...")
        
        # In a real scenario, these would be HDFS paths like:
        # employees_df = processor.read_csv_from_hdfs("hdfs://namenode:9000/user/data/employees.csv")
        # For demo purposes, reading from local files
        employees_df = processor.spark.read \
            .option("header", "true") \
            .option("inferSchema", "true") \
            .csv("/data/employees.csv")
        
        sales_df = processor.spark.read \
            .option("header", "true") \
            .option("inferSchema", "true") \
            .csv("/data/sales.csv")
        
        print(f"Employees data: {employees_df.count()} rows")
        print(f"Sales data: {sales_df.count()} rows")
        
        # Show schemas
        print("\nEmployees schema:")
        employees_df.printSchema()
        print("\nSales schema:")
        sales_df.printSchema()
        
        # Perform analyses
        salary_stats = processor.analyze_employees(employees_df)
        region_sales, product_sales = processor.analyze_sales(sales_df)
        performance = processor.join_employee_sales(employees_df, sales_df)
        data_mart = processor.create_data_mart(employees_df, sales_df)
        
        # Save results to HDFS (simulating with local output)
        print("\nSaving results...")
        
        # In real scenario, these would be HDFS paths:
        # processor.write_csv_to_hdfs(salary_stats, "hdfs://namenode:9000/user/output/salary_stats")
        # processor.write_parquet_to_hdfs(data_mart, "hdfs://namenode:9000/user/output/data_mart")
        
        # For demo, convert to Pandas and save locally
        print("Converting results to Pandas for local output...")
        salary_stats_pd = salary_stats.toPandas()
        data_mart_pd = data_mart.toPandas()
        
        print("\nSalary Statistics:")
        print(salary_stats_pd)
        print("\nData Mart:")
        print(data_mart_pd)
        
    except Exception as e:
        print(f"Error in main processing: {e}")
    
    finally:
        # Stop Spark session
        processor.stop_session()

if __name__ == "__main__":
    main()
