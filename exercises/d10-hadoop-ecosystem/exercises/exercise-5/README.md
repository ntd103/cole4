# Exercise 5: Python Integration and End-to-End Data Pipeline (Advanced Level)

## Objective
Create a complete data pipeline integrating Python with the entire Hadoop ecosystem, demonstrating real-world big data processing scenarios.

## Prerequisites
- All previous exercises (1-4) completed successfully
- Python environment with required libraries
- Jupyter Notebook accessible at http://localhost:8888

## Tasks

### Task 5.1: Python HDFS Integration (20 points)
Develop Python scripts to interact with HDFS for data management operations.

**Setup and Connection:**
```python
# Create hdfs_manager.py
import os
import sys
import pandas as pd
import json
from datetime import datetime

# Simulate HDFS operations (in real environment, use hdfs3 library)
class HDFSManager:
    def __init__(self, namenode_url="hdfs://namenode:9000"):
        self.namenode_url = namenode_url
        self.local_data_path = "/data/"
        print(f"Connected to HDFS: {namenode_url}")
    
    def upload_file(self, local_path, hdfs_path):
        """Upload file to HDFS"""
        # In real implementation: hdfs.put(local_path, hdfs_path)
        print(f"Uploaded {local_path} to {hdfs_path}")
        return True
    
    def download_file(self, hdfs_path, local_path):
        """Download file from HDFS"""
        # In real implementation: hdfs.get(hdfs_path, local_path)
        print(f"Downloaded {hdfs_path} to {local_path}")
        return True
    
    def list_directory(self, hdfs_path):
        """List HDFS directory contents"""
        # In real implementation: return hdfs.ls(hdfs_path)
        return [f"{hdfs_path}/file1.csv", f"{hdfs_path}/file2.csv"]
    
    def create_directory(self, hdfs_path):
        """Create HDFS directory"""
        print(f"Created directory: {hdfs_path}")
        return True

# Data processing functions
def process_employee_data(df):
    """Process employee data with business logic"""
    df['hire_year'] = pd.to_datetime(df['hire_date']).dt.year
    df['years_employed'] = datetime.now().year - df['hire_year']
    df['salary_category'] = pd.cut(df['salary'], 
                                  bins=[0, 50000, 75000, 100000, float('inf')],
                                  labels=['Entry', 'Mid', 'Senior', 'Executive'])
    return df

def process_sales_data(df):
    """Process sales data with analytics"""
    df['revenue'] = df['quantity'] * df['unit_price']
    df['sale_month'] = pd.to_datetime(df['sale_date']).dt.to_period('M')
    df['high_value_sale'] = df['revenue'] > df['revenue'].quantile(0.75)
    return df

# Main execution
if __name__ == "__main__":
    hdfs_manager = HDFSManager()
    
    # Create HDFS directory structure
    hdfs_manager.create_directory("/user/python/input")
    hdfs_manager.create_directory("/user/python/processed")
    hdfs_manager.create_directory("/user/python/output")
    
    # Load and process data
    employees_df = pd.read_csv("/data/employees.csv")
    sales_df = pd.read_csv("/data/sales.csv")
    
    # Process data
    employees_processed = process_employee_data(employees_df)
    sales_processed = process_sales_data(sales_df)
    
    # Save processed data
    employees_processed.to_csv("/tmp/employees_processed.csv", index=False)
    sales_processed.to_csv("/tmp/sales_processed.csv", index=False)
    
    # Upload to HDFS
    hdfs_manager.upload_file("/tmp/employees_processed.csv", "/user/python/processed/employees.csv")
    hdfs_manager.upload_file("/tmp/sales_processed.csv", "/user/python/processed/sales.csv")
    
    print("Data processing and HDFS upload completed!")
```

**Deliverable:**
- Complete Python script for HDFS operations
- Demonstration of data upload and processing
- Documentation of the data transformation logic

### Task 5.2: PySpark Data Processing (25 points)
Create PySpark applications for distributed data processing.

**PySpark Processing Script:**
```python
# Create pyspark_processor.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, expr, avg, sum as spark_sum, count, max as spark_max
from pyspark.sql.types import IntegerType, DoubleType
import pandas as pd

def create_spark_session():
    """Create Spark session with Hadoop configuration"""
    spark = SparkSession.builder \
        .appName("HadoopEcosystemIntegration") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9000") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("WARN")
    return spark

def advanced_employee_analysis(spark):
    """Perform advanced employee analytics"""
    # In real scenario: spark.read.csv("hdfs://namenode:9000/user/python/processed/employees.csv")
    employees_df = spark.read.csv("/data/employees.csv", header=True, inferSchema=True)
    
    # Advanced transformations
    employees_enhanced = employees_df.withColumn(
        "performance_tier",
        when(col("salary") > 80000, "High Performer")
        .when(col("salary") > 65000, "Good Performer")
        .otherwise("Standard Performer")
    ).withColumn(
        "department_size",
        expr("CASE WHEN department = 'Engineering' THEN 'Large' " +
             "WHEN department IN ('Marketing', 'Sales') THEN 'Medium' " +
             "ELSE 'Small' END")
    )
    
    # Department analytics
    dept_analytics = employees_enhanced.groupBy("department", "performance_tier").agg(
        count("employee_id").alias("employee_count"),
        avg("salary").alias("avg_salary"),
        spark_max("salary").alias("max_salary")
    ).orderBy("department", "performance_tier")
    
    return employees_enhanced, dept_analytics

def sales_trend_analysis(spark):
    """Analyze sales trends and patterns"""
    # In real scenario: read from HDFS
    sales_df = spark.read.csv("/data/sales.csv", header=True, inferSchema=True)
    
    # Add calculated columns
    sales_enhanced = sales_df.withColumn(
        "revenue", col("quantity") * col("unit_price")
    ).withColumn(
        "sale_category",
        when(col("quantity") * col("unit_price") > 1000, "High Value")
        .when(col("quantity") * col("unit_price") > 500, "Medium Value")
        .otherwise("Low Value")
    )
    
    # Trend analysis
    sales_trends = sales_enhanced.groupBy("region", "sale_category").agg(
        count("sale_id").alias("transaction_count"),
        spark_sum("revenue").alias("total_revenue"),
        avg("revenue").alias("avg_transaction_value")
    ).orderBy("region", col("total_revenue").desc())
    
    return sales_enhanced, sales_trends

def create_data_mart(employees_df, sales_df):
    """Create comprehensive data mart"""
    # Join employees and sales data
    employee_sales = employees_df.alias("e").join(
        sales_df.alias("s"),
        col("e.employee_id") == col("s.employee_id"),
        "left"
    )
    
    # Create comprehensive data mart
    data_mart = employee_sales.groupBy(
        "e.department", "s.region"
    ).agg(
        count("e.employee_id").alias("total_employees"),
        count("s.sale_id").alias("total_sales"),
        spark_sum("s.revenue").alias("total_revenue"),
        avg("e.salary").alias("avg_employee_salary")
    ).fillna(0)
    
    return data_mart

def main():
    """Main PySpark processing function"""
    spark = create_spark_session()
    
    try:
        # Employee analysis
        employees_enhanced, dept_analytics = advanced_employee_analysis(spark)
        print("Employee Analytics:")
        dept_analytics.show()
        
        # Sales analysis
        sales_enhanced, sales_trends = sales_trend_analysis(spark)
        print("Sales Trends:")
        sales_trends.show()
        
        # Data mart creation
        data_mart = create_data_mart(employees_enhanced, sales_enhanced)
        print("Data Mart:")
        data_mart.show()
        
        # Save results (in real scenario, save to HDFS)
        # data_mart.write.mode("overwrite").csv("hdfs://namenode:9000/user/python/output/data_mart")
        data_mart.coalesce(1).write.mode("overwrite").csv("/tmp/data_mart_output", header=True)
        
    finally:
        spark.stop()

if __name__ == "__main__":
    main()
```

**Deliverable:**
- Complete PySpark application
- Output of data processing results
- Performance analysis of distributed processing

### Task 5.3: HBase Integration with Python (20 points)
Develop Python applications to interact with HBase for real-time data access.

**HBase Python Integration:**
```python
# Create hbase_integration.py
import json
import random
from datetime import datetime, timedelta

# Simulate HBase operations (in real environment, use happybase library)
class HBaseManager:
    def __init__(self, host='hbase-master', port=9090):
        self.host = host
        self.port = port
        self.tables = {}  # Simulate in-memory storage
        print(f"Connected to HBase at {host}:{port}")
    
    def create_table(self, table_name, column_families):
        """Create HBase table with column families"""
        self.tables[table_name] = {}
        print(f"Created table '{table_name}' with families: {column_families}")
    
    def put_data(self, table_name, row_key, data):
        """Insert data into HBase table"""
        if table_name not in self.tables:
            self.tables[table_name] = {}
        self.tables[table_name][row_key] = data
        print(f"Inserted data for row key: {row_key}")
    
    def get_data(self, table_name, row_key):
        """Get data from HBase table"""
        if table_name in self.tables and row_key in self.tables[table_name]:
            return self.tables[table_name][row_key]
        return None
    
    def scan_table(self, table_name, limit=10):
        """Scan HBase table"""
        if table_name in self.tables:
            items = list(self.tables[table_name].items())[:limit]
            return items
        return []

def create_real_time_analytics_tables(hbase_manager):
    """Create tables for real-time analytics"""
    # Employee activity tracking
    hbase_manager.create_table('employee_activity', 
                              ['session', 'performance', 'alerts'])
    
    # Sales real-time metrics
    hbase_manager.create_table('sales_metrics', 
                              ['hourly', 'daily', 'alerts'])
    
    # Customer engagement tracking
    hbase_manager.create_table('customer_engagement', 
                              ['activity', 'preferences', 'scores'])

def simulate_real_time_data(hbase_manager):
    """Simulate real-time data ingestion"""
    # Employee activity simulation
    for emp_id in range(1001, 1011):
        row_key = f"emp_{emp_id}_{datetime.now().strftime('%Y%m%d')}"
        activity_data = {
            'session:login_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'session:last_activity': (datetime.now() - timedelta(minutes=random.randint(1, 60))).strftime('%Y-%m-%d %H:%M:%S'),
            'performance:tasks_completed': str(random.randint(5, 20)),
            'performance:productivity_score': str(random.uniform(0.7, 1.0)),
            'alerts:late_login': str(random.choice([True, False]))
        }
        hbase_manager.put_data('employee_activity', row_key, activity_data)
    
    # Sales metrics simulation
    for hour in range(24):
        row_key = f"sales_{datetime.now().strftime('%Y%m%d')}_{hour:02d}"
        sales_data = {
            'hourly:transaction_count': str(random.randint(10, 50)),
            'hourly:revenue': str(random.uniform(1000, 5000)),
            'daily:cumulative_revenue': str(random.uniform(10000, 50000)),
            'alerts:low_performance': str(random.choice([True, False]))
        }
        hbase_manager.put_data('sales_metrics', row_key, sales_data)

def analyze_real_time_data(hbase_manager):
    """Analyze real-time data from HBase"""
    print("\n=== Real-time Employee Activity Analysis ===")
    employee_activities = hbase_manager.scan_table('employee_activity')
    
    total_productivity = 0
    alert_count = 0
    
    for row_key, data in employee_activities:
        productivity = float(data.get('performance:productivity_score', 0))
        total_productivity += productivity
        
        if data.get('alerts:late_login') == 'True':
            alert_count += 1
        
        print(f"Employee {row_key}: Productivity {productivity:.2f}")
    
    avg_productivity = total_productivity / len(employee_activities) if employee_activities else 0
    print(f"Average Productivity: {avg_productivity:.2f}")
    print(f"Late Login Alerts: {alert_count}")
    
    print("\n=== Real-time Sales Metrics Analysis ===")
    sales_metrics = hbase_manager.scan_table('sales_metrics')
    
    total_revenue = 0
    total_transactions = 0
    
    for row_key, data in sales_metrics:
        revenue = float(data.get('hourly:revenue', 0))
        transactions = int(data.get('hourly:transaction_count', 0))
        
        total_revenue += revenue
        total_transactions += transactions
        
        print(f"Hour {row_key}: Revenue ${revenue:.2f}, Transactions {transactions}")
    
    print(f"Total Revenue: ${total_revenue:.2f}")
    print(f"Total Transactions: {total_transactions}")

def main():
    """Main HBase integration function"""
    hbase_manager = HBaseManager()
    
    # Create tables
    create_real_time_analytics_tables(hbase_manager)
    
    # Simulate real-time data ingestion
    simulate_real_time_data(hbase_manager)
    
    # Analyze data
    analyze_real_time_data(hbase_manager)

if __name__ == "__main__":
    main()
```

**Deliverable:**
- HBase Python integration script
- Real-time data simulation and analysis
- Documentation of NoSQL data modeling decisions

### Task 5.4: End-to-End Data Pipeline (25 points)
Create a complete data pipeline orchestrating all Hadoop ecosystem components.

**Pipeline Orchestrator:**
```python
# Create data_pipeline.py
import subprocess
import time
import json
from datetime import datetime
import pandas as pd

class HadoopDataPipeline:
    def __init__(self):
        self.pipeline_start_time = datetime.now()
        self.pipeline_status = {}
        
    def log_step(self, step_name, status, message=""):
        """Log pipeline step execution"""
        self.pipeline_status[step_name] = {
            'status': status,
            'timestamp': datetime.now().isoformat(),
            'message': message
        }
        print(f"[{datetime.now()}] {step_name}: {status} - {message}")
    
    def extract_from_mysql(self):
        """Step 1: Extract data from MySQL using Sqoop"""
        self.log_step("extract_mysql", "STARTED", "Extracting data from MySQL")
        
        try:
            # Simulate Sqoop import
            # In real implementation: run sqoop import commands
            time.sleep(2)  # Simulate processing time
            self.log_step("extract_mysql", "COMPLETED", "Data extracted successfully")
            return True
        except Exception as e:
            self.log_step("extract_mysql", "FAILED", str(e))
            return False
    
    def process_with_spark(self):
        """Step 2: Process data with PySpark"""
        self.log_step("spark_processing", "STARTED", "Processing data with Spark")
        
        try:
            # Load and process data
            employees_df = pd.read_csv("/data/employees.csv")
            sales_df = pd.read_csv("/data/sales.csv")
            
            # Business logic processing
            employees_df['performance_score'] = employees_df['salary'] / employees_df['salary'].max()
            sales_df['revenue'] = sales_df['quantity'] * sales_df['unit_price']
            
            # Save processed data
            employees_df.to_csv("/tmp/employees_processed_pipeline.csv", index=False)
            sales_df.to_csv("/tmp/sales_processed_pipeline.csv", index=False)
            
            self.log_step("spark_processing", "COMPLETED", f"Processed {len(employees_df)} employees, {len(sales_df)} sales records")
            return True
        except Exception as e:
            self.log_step("spark_processing", "FAILED", str(e))
            return False
    
    def load_to_hive(self):
        """Step 3: Load processed data to Hive"""
        self.log_step("hive_loading", "STARTED", "Loading data to Hive tables")
        
        try:
            # Simulate Hive table creation and data loading
            # In real implementation: execute Hive DDL and DML commands
            time.sleep(3)  # Simulate processing time
            self.log_step("hive_loading", "COMPLETED", "Data loaded to Hive warehouse")
            return True
        except Exception as e:
            self.log_step("hive_loading", "FAILED", str(e))
            return False
    
    def update_hbase_metrics(self):
        """Step 4: Update real-time metrics in HBase"""
        self.log_step("hbase_update", "STARTED", "Updating HBase metrics")
        
        try:
            # Calculate and store real-time metrics
            employees_df = pd.read_csv("/tmp/employees_processed_pipeline.csv")
            sales_df = pd.read_csv("/tmp/sales_processed_pipeline.csv")
            
            # Calculate metrics
            metrics = {
                'total_employees': len(employees_df),
                'avg_salary': employees_df['salary'].mean(),
                'total_sales': len(sales_df),
                'total_revenue': sales_df['revenue'].sum(),
                'pipeline_timestamp': datetime.now().isoformat()
            }
            
            # Save metrics (simulate HBase storage)
            with open("/tmp/hbase_metrics.json", "w") as f:
                json.dump(metrics, f, indent=2)
            
            self.log_step("hbase_update", "COMPLETED", f"Updated metrics: {len(metrics)} KPIs")
            return True
        except Exception as e:
            self.log_step("hbase_update", "FAILED", str(e))
            return False
    
    def generate_reports(self):
        """Step 5: Generate analysis reports"""
        self.log_step("report_generation", "STARTED", "Generating analysis reports")
        
        try:
            # Load processed data
            employees_df = pd.read_csv("/tmp/employees_processed_pipeline.csv")
            sales_df = pd.read_csv("/tmp/sales_processed_pipeline.csv")
            
            # Generate department summary
            dept_summary = employees_df.groupby('department').agg({
                'employee_id': 'count',
                'salary': ['mean', 'max', 'min'],
                'performance_score': 'mean'
            }).round(2)
            
            # Generate sales summary
            sales_summary = sales_df.groupby('region').agg({
                'sale_id': 'count',
                'revenue': ['sum', 'mean'],
                'quantity': 'sum'
            }).round(2)
            
            # Save reports
            dept_summary.to_csv("/tmp/department_report.csv")
            sales_summary.to_csv("/tmp/sales_report.csv")
            
            # Create executive summary
            exec_summary = {
                'pipeline_execution_time': (datetime.now() - self.pipeline_start_time).total_seconds(),
                'total_departments': len(dept_summary),
                'total_regions': len(sales_summary),
                'highest_revenue_region': sales_summary['revenue']['sum'].idxmax(),
                'highest_paid_department': dept_summary['salary']['mean'].idxmax()
            }
            
            with open("/tmp/executive_summary.json", "w") as f:
                json.dump(exec_summary, f, indent=2)
            
            self.log_step("report_generation", "COMPLETED", "Reports generated successfully")
            return True
        except Exception as e:
            self.log_step("report_generation", "FAILED", str(e))
            return False
    
    def run_pipeline(self):
        """Execute the complete data pipeline"""
        print("="*60)
        print("HADOOP ECOSYSTEM DATA PIPELINE EXECUTION")
        print("="*60)
        
        pipeline_steps = [
            ("extract_from_mysql", self.extract_from_mysql),
            ("process_with_spark", self.process_with_spark),
            ("load_to_hive", self.load_to_hive),
            ("update_hbase_metrics", self.update_hbase_metrics),
            ("generate_reports", self.generate_reports)
        ]
        
        for step_name, step_function in pipeline_steps:
            success = step_function()
            if not success:
                print(f"Pipeline failed at step: {step_name}")
                return False
        
        # Pipeline completion summary
        total_time = (datetime.now() - self.pipeline_start_time).total_seconds()
        print("\n" + "="*60)
        print("PIPELINE EXECUTION SUMMARY")
        print("="*60)
        print(f"Total execution time: {total_time:.2f} seconds")
        print(f"Pipeline status: SUCCESS")
        
        for step, details in self.pipeline_status.items():
            print(f"  {step}: {details['status']} at {details['timestamp']}")
        
        return True

def main():
    """Main pipeline execution"""
    pipeline = HadoopDataPipeline()
    success = pipeline.run_pipeline()
    
    if success:
        print("\nPipeline completed successfully!")
        print("Output files:")
        print("  - /tmp/employees_processed_pipeline.csv")
        print("  - /tmp/sales_processed_pipeline.csv")
        print("  - /tmp/department_report.csv")
        print("  - /tmp/sales_report.csv")
        print("  - /tmp/executive_summary.json")
        print("  - /tmp/hbase_metrics.json")
    else:
        print("\nPipeline execution failed!")

if __name__ == "__main__":
    main()
```

**Deliverable:**
- Complete data pipeline implementation
- Pipeline execution logs and results
- Data lineage documentation
- Performance metrics and optimization recommendations

### Task 5.5: Jupyter Notebook Analysis (10 points)
Create a comprehensive Jupyter notebook demonstrating the integration results.

**Use the provided notebook template and extend it with:**
1. Pipeline execution results visualization
2. Comparative analysis between different storage systems
3. Performance benchmarking
4. Business insights and recommendations

## Final Deliverables

Create a folder named `exercise5_[your_name]` containing:

1. **scripts/** folder with all Python scripts
2. **notebooks/** folder with completed Jupyter notebooks
3. **outputs/** folder with all generated reports and data files
4. **pipeline_documentation.md** - Complete pipeline documentation (minimum 800 words)
5. **performance_analysis.md** - Performance comparison across components (minimum 500 words)
6. **business_insights.md** - Business insights and recommendations (minimum 400 words)
7. **integration_architecture.md** - Technical architecture documentation (minimum 600 words)
8. **reflection.md** - Overall learning experience and future improvements (minimum 400 words)

## Grading Rubric

| Component | Points | Criteria |
|-----------|---------|----------|
| Task 5.1 | 20 | Python HDFS integration working correctly |
| Task 5.2 | 25 | PySpark processing implemented successfully |
| Task 5.3 | 20 | HBase integration functional |
| Task 5.4 | 25 | Complete pipeline orchestration working |
| Task 5.5 | 10 | Comprehensive notebook analysis |
| **Total** | **100** | |

## Success Criteria

1. **Technical Implementation**: All scripts execute without errors
2. **Data Quality**: Data integrity maintained throughout pipeline
3. **Performance**: Reasonable execution times for data processing
4. **Documentation**: Clear, comprehensive documentation
5. **Business Value**: Actionable insights generated from analysis

## Bonus Opportunities (+15 points)

1. **Error Handling**: Implement robust error handling and recovery (5 points)
2. **Monitoring**: Add pipeline monitoring and alerting (5 points)
3. **Optimization**: Performance optimization implementations (5 points)

## Additional Resources
- [Python Big Data Processing](https://spark.apache.org/docs/latest/api/python/)
- [Hadoop Ecosystem Integration Patterns](https://hadoop.apache.org/docs/stable/)
- [Data Pipeline Best Practices](https://databricks.com/)
