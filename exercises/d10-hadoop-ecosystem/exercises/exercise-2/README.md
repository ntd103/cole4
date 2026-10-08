# Exercise 2: Hive Data Warehousing (Intermediate Level)

## Objective
Learn Hive data warehousing concepts including table creation, data loading, partitioning, and complex SQL queries.

## Prerequisites
- Exercise 1 completed successfully
- Hive Server2 running and accessible
- Sample data uploaded to HDFS

## Tasks

### Task 2.1: Database and Table Creation (25 points)
Create a Hive database and tables for our data warehouse.

**Connect to Hive:**
```bash
# Access hive-server container
docker exec -it hive-server bash

# Connect to Hive CLI
beeline -u jdbc:hive2://localhost:10000
```

**SQL Commands:**
```sql
-- Create database
CREATE DATABASE IF NOT EXISTS company_dw;
USE company_dw;

-- Create external table for employees
CREATE EXTERNAL TABLE employees_ext (
    employee_id INT,
    first_name STRING,
    last_name STRING,
    email STRING,
    department STRING,
    salary DOUBLE,
    hire_date DATE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/student/input/'
TBLPROPERTIES ('skip.header.line.count'='1');

-- Create managed table for processed employees
CREATE TABLE employees_managed (
    employee_id INT,
    first_name STRING,
    last_name STRING,
    email STRING,
    department STRING,
    salary DOUBLE,
    hire_date DATE,
    years_experience INT
)
STORED AS PARQUET;

-- Show tables
SHOW TABLES;
DESCRIBE employees_ext;
```

**Deliverable:** 
- Screenshot of table creation outputs
- Screenshot of table descriptions

### Task 2.2: Data Loading and ETL (30 points)
Load data into tables and perform ETL operations.

**SQL Commands:**
```sql
-- Load data from external table to managed table with transformation
INSERT INTO employees_managed
SELECT 
    employee_id,
    first_name,
    last_name,
    email,
    department,
    salary,
    hire_date,
    CAST(DATEDIFF(CURRENT_DATE, hire_date) / 365 AS INT) as years_experience
FROM employees_ext;

-- Create sales table
CREATE EXTERNAL TABLE sales_ext (
    sale_id INT,
    employee_id INT,
    customer_id INT,
    product_name STRING,
    quantity INT,
    unit_price DOUBLE,
    sale_date DATE,
    region STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/student/input/'
TBLPROPERTIES ('skip.header.line.count'='1');

-- Create sales fact table with calculated revenue
CREATE TABLE sales_fact AS
SELECT 
    sale_id,
    employee_id,
    customer_id,
    product_name,
    quantity,
    unit_price,
    (quantity * unit_price) as revenue,
    sale_date,
    region,
    YEAR(sale_date) as sale_year,
    MONTH(sale_date) as sale_month
FROM sales_ext;

-- Verify data loading
SELECT COUNT(*) FROM employees_managed;
SELECT COUNT(*) FROM sales_fact;
```

**Deliverable:**
- SQL script file with all commands
- Screenshot of row counts for verification

### Task 2.3: Complex Analytical Queries (35 points)
Write and execute complex SQL queries to analyze the data.

**Query 1: Department Performance Analysis**
```sql
-- Department statistics with ranking
SELECT 
    department,
    COUNT(*) as employee_count,
    AVG(salary) as avg_salary,
    MAX(salary) as max_salary,
    MIN(salary) as min_salary,
    STDDEV(salary) as salary_stddev,
    RANK() OVER (ORDER BY AVG(salary) DESC) as salary_rank
FROM employees_managed
GROUP BY department
ORDER BY avg_salary DESC;
```

**Query 2: Sales Performance Analysis**
```sql
-- Employee sales performance with joins
SELECT 
    e.employee_id,
    e.first_name,
    e.last_name,
    e.department,
    COUNT(s.sale_id) as total_sales,
    SUM(s.revenue) as total_revenue,
    AVG(s.revenue) as avg_sale_value,
    MAX(s.sale_date) as last_sale_date
FROM employees_managed e
LEFT JOIN sales_fact s ON e.employee_id = s.employee_id
GROUP BY e.employee_id, e.first_name, e.last_name, e.department
ORDER BY total_revenue DESC;
```

**Query 3: Time-based Analysis**
```sql
-- Monthly sales trend analysis
SELECT 
    sale_year,
    sale_month,
    region,
    COUNT(*) as num_sales,
    SUM(revenue) as total_revenue,
    AVG(revenue) as avg_revenue,
    LAG(SUM(revenue)) OVER (PARTITION BY region ORDER BY sale_year, sale_month) as prev_month_revenue,
    ((SUM(revenue) - LAG(SUM(revenue)) OVER (PARTITION BY region ORDER BY sale_year, sale_month)) / 
     LAG(SUM(revenue)) OVER (PARTITION BY region ORDER BY sale_year, sale_month)) * 100 as revenue_growth_pct
FROM sales_fact
GROUP BY sale_year, sale_month, region
ORDER BY region, sale_year, sale_month;
```

**Query 4: Product Analysis**
```sql
-- Product performance with statistical functions
SELECT 
    product_name,
    COUNT(*) as sales_count,
    SUM(quantity) as total_quantity_sold,
    SUM(revenue) as total_revenue,
    AVG(unit_price) as avg_unit_price,
    PERCENTILE_APPROX(revenue, 0.5) as median_revenue,
    COLLECT_LIST(region) as regions_sold
FROM sales_fact
GROUP BY product_name
ORDER BY total_revenue DESC;
```

**Query 5: Advanced Analytics**
```sql
-- Create a comprehensive business intelligence view
CREATE VIEW business_intelligence AS
SELECT 
    s.sale_id,
    s.sale_date,
    s.product_name,
    s.quantity,
    s.unit_price,
    s.revenue,
    s.region,
    e.first_name || ' ' || e.last_name as employee_name,
    e.department,
    e.salary as employee_salary,
    ROW_NUMBER() OVER (PARTITION BY s.sale_date ORDER BY s.revenue DESC) as daily_sales_rank,
    SUM(s.revenue) OVER (PARTITION BY e.employee_id) as employee_total_revenue,
    AVG(s.revenue) OVER (PARTITION BY s.product_name) as product_avg_revenue
FROM sales_fact s
JOIN employees_managed e ON s.employee_id = e.employee_id;

-- Query the view
SELECT * FROM business_intelligence WHERE daily_sales_rank <= 3;
```

**Deliverable:**
- Text file with all query results
- Analysis document explaining insights found in each query

### Task 2.4: Partitioning and Optimization (10 points)
Create partitioned tables for better performance.

**SQL Commands:**
```sql
-- Create partitioned sales table
CREATE TABLE sales_partitioned (
    sale_id INT,
    employee_id INT,
    customer_id INT,
    product_name STRING,
    quantity INT,
    unit_price DOUBLE,
    revenue DOUBLE,
    sale_date DATE
)
PARTITIONED BY (region STRING, sale_year INT)
STORED AS PARQUET;

-- Enable dynamic partitioning
SET hive.exec.dynamic.partition = true;
SET hive.exec.dynamic.partition.mode = nonstrict;

-- Load data into partitioned table
INSERT INTO sales_partitioned PARTITION(region, sale_year)
SELECT 
    sale_id,
    employee_id,
    customer_id,
    product_name,
    quantity,
    unit_price,
    revenue,
    sale_date,
    region,
    sale_year
FROM sales_fact;

-- Show partitions
SHOW PARTITIONS sales_partitioned;

-- Query specific partition
SELECT COUNT(*) FROM sales_partitioned WHERE region = 'North' AND sale_year = 2024;
```

**Deliverable:**
- Screenshot of partition information
- Explanation of partitioning benefits

## Submission Requirements

Create a folder named `exercise2_[your_name]` containing:

1. **sql_scripts/** folder with all SQL files
2. **query_results/** folder with all query outputs
3. **screenshots/** folder with required screenshots
4. **analysis_report.md** - Detailed analysis of findings (minimum 500 words)
5. **optimization_report.md** - Discussion of partitioning and performance (minimum 300 words)
6. **reflection.md** - Learning outcomes and challenges (minimum 200 words)

## Grading Rubric

| Component | Points | Criteria |
|-----------|---------|----------|
| Task 2.1 | 25 | Tables created correctly with proper schemas |
| Task 2.2 | 30 | Data loaded successfully with ETL transformations |
| Task 2.3 | 35 | All complex queries executed with correct results |
| Task 2.4 | 10 | Partitioning implemented and explained |
| **Total** | **100** | |

## Tips for Success

1. **Query Optimization**: Use EXPLAIN PLAN to understand query execution
2. **Data Validation**: Always verify row counts after data loading
3. **Error Handling**: Check Hive logs if queries fail
4. **Performance**: Monitor query execution time for optimization opportunities

## Common Issues and Solutions

1. **Table Not Found**: Ensure you're in the correct database
2. **Permission Errors**: Check HDFS permissions for data files
3. **Memory Issues**: Increase container memory if queries fail
4. **Date Format**: Ensure date formats match your data

## Additional Resources
- [Hive Language Manual](https://cwiki.apache.org/confluence/display/Hive/LanguageManual)
- [Hive Performance Tuning](https://cwiki.apache.org/confluence/display/Hive/Configuration+Properties)
