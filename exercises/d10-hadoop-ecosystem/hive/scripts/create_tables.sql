-- Create employee table
CREATE EXTERNAL TABLE IF NOT EXISTS employees (
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
LOCATION '/user/hive/warehouse/employees'
TBLPROPERTIES ('skip.header.line.count'='1');

-- Create sales table
CREATE EXTERNAL TABLE IF NOT EXISTS sales (
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
LOCATION '/user/hive/warehouse/sales'
TBLPROPERTIES ('skip.header.line.count'='1');

-- Create customers table for JSON data
CREATE EXTERNAL TABLE IF NOT EXISTS customers (
    customer_id INT,
    name STRING,
    email STRING,
    phone STRING,
    street STRING,
    city STRING,
    state STRING,
    zip STRING,
    registration_date DATE,
    customer_type STRING
)
ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
STORED AS TEXTFILE
LOCATION '/user/hive/warehouse/customers';

-- Load data into tables
LOAD DATA INPATH '/user/hive/warehouse/demo/employees.csv' INTO TABLE employees;
LOAD DATA INPATH '/user/hive/warehouse/demo/sales.csv' INTO TABLE sales;
LOAD DATA INPATH '/user/hive/warehouse/demo/customers.json' INTO TABLE customers;
