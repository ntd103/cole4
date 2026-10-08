# Exercise 4: Data Integration with Sqoop (Advanced Level)

## Objective
Master data integration between relational databases and Hadoop ecosystem using Apache Sqoop for ETL operations.

## Prerequisites
- Exercises 1, 2, and 3 completed
- MySQL database running with sample data
- Understanding of HDFS and Hive tables

## Tasks

### Task 4.1: Database Connectivity and Exploration (20 points)
Establish connection to MySQL and explore the database structure.

**Connect to Sqoop:**
```bash
# Access sqoop container
docker exec -it sqoop bash

# Test MySQL connectivity
sqoop list-databases \
--connect jdbc:mysql://mysql:3306/ \
--username sqoop \
--password sqoop

# List tables in testdb
sqoop list-tables \
--connect jdbc:mysql://mysql:3306/testdb \
--username sqoop \
--password sqoop

# Evaluate a table (check table structure and sample data)
sqoop eval \
--connect jdbc:mysql://mysql:3306/testdb \
--username sqoop \
--password sqoop \
--query "DESCRIBE employees"

sqoop eval \
--connect jdbc:mysql://mysql:3306/testdb \
--username sqoop \
--password sqoop \
--query "SELECT * FROM employees LIMIT 5"
```

**Deliverable:**
- Screenshots of database and table listings
- Output of table structure and sample data

### Task 4.2: Basic Import Operations (25 points)
Import data from MySQL to HDFS using various Sqoop import strategies.

**Full Table Import:**
```bash
# Import entire employees table
sqoop import \
--connect jdbc:mysql://mysql:3306/testdb \
--username sqoop \
--password sqoop \
--table employees \
--target-dir /user/sqoop/import/employees_full \
--num-mappers 1 \
--delete-target-dir

# Verify the import
hdfs dfs -ls /user/sqoop/import/employees_full
hdfs dfs -head /user/sqoop/import/employees_full/part-m-00000
```

**Selective Column Import:**
```bash
# Import specific columns only
sqoop import \
--connect jdbc:mysql://mysql:3306/testdb \
--username sqoop \
--password sqoop \
--table employees \
--columns "employee_id,first_name,last_name,department,salary" \
--target-dir /user/sqoop/import/employees_selective \
--num-mappers 1 \
--delete-target-dir

# Import with WHERE clause
sqoop import \
--connect jdbc:mysql://mysql:3306/testdb \
--username sqoop \
--password sqoop \
--table employees \
--where "department='Engineering' AND salary > 70000" \
--target-dir /user/sqoop/import/employees_filtered \
--num-mappers 1 \
--delete-target-dir
```

**Custom Query Import:**
```bash
# Import using custom SQL query
sqoop import \
--connect jdbc:mysql://mysql:3306/testdb \
--username sqoop \
--password sqoop \
--query "SELECT e.employee_id, e.first_name, e.last_name, e.department, e.salary, COUNT(s.sale_id) as sales_count FROM employees e LEFT JOIN sales s ON e.employee_id = s.employee_id GROUP BY e.employee_id, e.first_name, e.last_name, e.department, e.salary AND \$CONDITIONS" \
--target-dir /user/sqoop/import/employee_sales_summary \
--split-by e.employee_id \
--num-mappers 2 \
--delete-target-dir
```

**Deliverable:**
- Command execution logs
- Screenshots of HDFS directories with imported data
- Sample of imported data content

### Task 4.3: Advanced Import Techniques (25 points)
Implement advanced import strategies including incremental imports and different file formats.

**Parquet Format Import:**
```bash
# Import as Parquet format
sqoop import \
--connect jdbc:mysql://mysql:3306/testdb \
--username sqoop \
--password sqoop \
--table sales \
--target-dir /user/sqoop/import/sales_parquet \
--as-parquetfile \
--num-mappers 1 \
--delete-target-dir

# Verify Parquet files
hdfs dfs -ls /user/sqoop/import/sales_parquet
```

**Avro Format Import:**
```bash
# Import as Avro format
sqoop import \
--connect jdbc:mysql://mysql:3306/testdb \
--username sqoop \
--password sqoop \
--table customers \
--target-dir /user/sqoop/import/customers_avro \
--as-avrodatafile \
--num-mappers 1 \
--delete-target-dir

# Check Avro schema
hdfs dfs -ls /user/sqoop/import/customers_avro
```

**Incremental Import Setup:**
```bash
# Initial import with last-modified strategy
sqoop import \
--connect jdbc:mysql://mysql:3306/testdb \
--username sqoop \
--password sqloop \
--table sales \
--target-dir /user/sqoop/import/sales_incremental \
--incremental lastmodified \
--check-column sale_date \
--last-value "2024-01-01" \
--num-mappers 1

# Simulate incremental update (add new data to MySQL first)
# Add new records to MySQL
sqoop eval \
--connect jdbc:mysql://mysql:3306/testdb \
--username sqoop \
--password sqoop \
--query "INSERT INTO sales VALUES (2011, 1004, 5001, 'Webcam', 1, 150.00, '2024-01-25', 'North')"

# Run incremental import
sqoop import \
--connect jdbc:mysql://mysql:3306/testdb \
--username sqoop \
--password sqoop \
--table sales \
--target-dir /user/sqoop/import/sales_incremental \
--incremental lastmodified \
--check-column sale_date \
--last-value "2024-01-24" \
--append
```

**Compressed Import:**
```bash
# Import with compression
sqoop import \
--connect jdbc:mysql://mysql:3306/testdb \
--username sqoop \
--password sqoop \
--table employees \
--target-dir /user/sqoop/import/employees_compressed \
--compression-codec gzip \
--num-mappers 1 \
--delete-target-dir
```

**Deliverable:**
- Comparison of file sizes for different formats
- Verification of incremental import functionality
- Performance analysis of different import strategies

### Task 4.4: Import to Hive Integration (15 points)
Import data directly into Hive tables using Sqoop.

**Direct Hive Import:**
```bash
# Import directly to Hive table
sqoop import \
--connect jdbc:mysql://mysql:3306/testdb \
--username sqoop \
--password sqoop \
--table employees \
--hive-import \
--hive-table sqoop_demo.employees_from_mysql \
--create-hive-table \
--hive-overwrite \
--num-mappers 1

# Import to existing Hive table
sqoop import \
--connect jdbc:mysql://mysql:3306/testdb \
--username sqoop \
--password sqoop \
--table sales \
--hive-import \
--hive-table sqoop_demo.sales_from_mysql \
--create-hive-table \
--num-mappers 1
```

**Verify in Hive:**
```bash
# Connect to Hive and verify data
docker exec -it hive-server bash
beeline -u jdbc:hive2://localhost:10000

# In Hive:
USE sqoop_demo;
SHOW TABLES;
SELECT COUNT(*) FROM employees_from_mysql;
SELECT * FROM employees_from_mysql LIMIT 5;
```

**Deliverable:**
- Screenshots of Hive tables created by Sqoop
- Verification of data integrity between MySQL and Hive

### Task 4.5: Export Operations (15 points)
Export processed data from Hadoop back to MySQL.

**Prepare Export Target:**
```bash
# Create target table in MySQL
sqoop eval \
--connect jdbc:mysql://mysql:3306/testdb \
--username sqoop \
--password sqoop \
--query "CREATE TABLE employee_summary_export (
    department VARCHAR(50),
    employee_count INT,
    avg_salary DECIMAL(10,2),
    max_salary DECIMAL(10,2),
    min_salary DECIMAL(10,2)
)"
```

**Create Summary Data in Hive:**
```sql
-- In Hive, create summary data
USE company_dw;

CREATE TABLE department_summary AS
SELECT 
    department,
    COUNT(*) as employee_count,
    AVG(salary) as avg_salary,
    MAX(salary) as max_salary,
    MIN(salary) as min_salary
FROM employees_managed
GROUP BY department;

-- Export to HDFS location
INSERT OVERWRITE DIRECTORY '/user/sqloop/export/department_summary'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
SELECT * FROM department_summary;
```

**Export to MySQL:**
```bash
# Export processed data back to MySQL
sqoop export \
--connect jdbc:mysql://mysql:3306/testdb \
--username sqoop \
--password sqoop \
--table employee_summary_export \
--export-dir /user/sqoop/export/department_summary \
--input-fields-terminated-by ',' \
--num-mappers 1

# Verify export
sqoop eval \
--connect jdbc:mysql://mysql:3306/testdb \
--username sqoop \
--password sqoop \
--query "SELECT * FROM employee_summary_export"
```

**Update Export:**
```bash
# Create table for update operations
sqoop eval \
--connect jdbc:mysql://mysql:3306/testdb \
--username sqoop \
--password sqoop \
--query "CREATE TABLE employees_updated AS SELECT * FROM employees"

# Export with update mode
sqoop export \
--connect jdbc:mysql://mysql:3306/testdb \
--username sqoop \
--password sqoop \
--table employees_updated \
--export-dir /user/sqoop/import/employees_full \
--update-key employee_id \
--update-mode updateonly \
--input-fields-terminated-by ',' \
--num-mappers 1
```

**Deliverable:**
- Screenshots of MySQL tables after export
- Verification of data consistency
- Documentation of export process

## Advanced Challenges (Bonus - 10 points)

### Challenge 1: Sqoop Job Creation
Create and manage Sqoop jobs for automation:

```bash
# Create a Sqoop job
sqoop job --create import_employees -- import \
--connect jdbc:mysql://mysql:3306/testdb \
--username sqoop \
--password sqoop \
--table employees \
--target-dir /user/sqoop/jobs/employees \
--delete-target-dir

# List jobs
sqoop job --list

# Execute job
sqoop job --exec import_employees

# Show job details
sqoop job --show import_employees
```

### Challenge 2: Performance Optimization
Optimize Sqoop imports for better performance:

```bash
# Parallel import with multiple mappers
sqoop import \
--connect jdbc:mysql://mysql:3306/testdb \
--username sqoop \
--password sqoop \
--table sales \
--target-dir /user/sqoop/performance/sales_parallel \
--split-by sale_id \
--num-mappers 4 \
--delete-target-dir

# Compare performance with single mapper
```

## Submission Requirements

Create a folder named `exercise4_[your_name]` containing:

1. **sqoop_commands/** folder with all command scripts
2. **outputs/** folder with command results and screenshots
3. **data_verification/** folder with before/after data samples
4. **integration_report.md** - Data integration analysis (minimum 500 words)
5. **performance_analysis.md** - Import/export performance comparison (minimum 300 words)
6. **troubleshooting_log.md** - Issues encountered and solutions (minimum 200 words)
7. **reflection.md** - Learning outcomes and ETL best practices (minimum 300 words)

## Grading Rubric

| Component | Points | Criteria |
|-----------|---------|----------|
| Task 4.1 | 20 | Database connectivity and exploration |
| Task 4.2 | 25 | Basic import operations working correctly |
| Task 4.3 | 25 | Advanced import techniques implemented |
| Task 4.4 | 15 | Hive integration successful |
| Task 4.5 | 15 | Export operations completed |
| Bonus | 10 | Advanced challenges attempted |
| **Total** | **110** | |

## Key Learning Objectives

1. **Data Integration**: Moving data between different systems
2. **ETL Processes**: Extract, Transform, Load operations
3. **Performance Optimization**: Parallel processing and format selection
4. **Incremental Updates**: Handling data changes over time
5. **Data Validation**: Ensuring data integrity across systems

## Common Issues and Solutions

1. **Connection Errors**: Check MySQL container status and network connectivity
2. **Permission Issues**: Verify database user permissions
3. **Memory Problems**: Adjust mapper count based on available resources
4. **Data Type Mismatches**: Handle data type conversions properly
5. **Performance Issues**: Optimize split-by columns and mapper count

## Best Practices

1. **Connection Pooling**: Reuse database connections
2. **Parallel Processing**: Use appropriate number of mappers
3. **Data Validation**: Always verify imported data
4. **Error Handling**: Implement proper error recovery
5. **Monitoring**: Track import/export performance
6. **Security**: Use secure password handling

## Additional Resources
- [Sqoop User Guide](https://sqoop.apache.org/docs/1.4.7/SqoopUserGuide.html)
- [Sqoop Performance Tuning](https://sqoop.apache.org/docs/1.4.7/SqoopUserGuide.html#_performance_tuning)
- [Hadoop Data Ingestion Patterns](https://hadoop.apache.org/)
