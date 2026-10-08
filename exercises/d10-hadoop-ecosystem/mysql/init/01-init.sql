-- Initialize MySQL database with sample data for Sqoop demonstrations

USE testdb;

-- Create employees table
CREATE TABLE IF NOT EXISTS employees (
    employee_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    department VARCHAR(50),
    salary DECIMAL(10,2),
    hire_date DATE
);

-- Create sales table
CREATE TABLE IF NOT EXISTS sales (
    sale_id INT PRIMARY KEY,
    employee_id INT,
    customer_id INT,
    product_name VARCHAR(100),
    quantity INT,
    unit_price DECIMAL(10,2),
    sale_date DATE,
    region VARCHAR(50)
);

-- Create customers table
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    address TEXT,
    city VARCHAR(50),
    state VARCHAR(20),
    zip VARCHAR(10),
    registration_date DATE,
    customer_type VARCHAR(20)
);

-- Insert sample employees data
INSERT INTO employees VALUES
(1001, 'John', 'Smith', 'john.smith@company.com', 'Engineering', 75000.00, '2020-01-15'),
(1002, 'Jane', 'Doe', 'jane.doe@company.com', 'Marketing', 65000.00, '2020-02-20'),
(1003, 'Bob', 'Johnson', 'bob.johnson@company.com', 'Engineering', 80000.00, '2019-11-10'),
(1004, 'Alice', 'Williams', 'alice.williams@company.com', 'Sales', 70000.00, '2021-03-05'),
(1005, 'Charlie', 'Brown', 'charlie.brown@company.com', 'HR', 60000.00, '2020-07-12'),
(1006, 'Diana', 'Davis', 'diana.davis@company.com', 'Engineering', 82000.00, '2019-09-18'),
(1007, 'Eve', 'Miller', 'eve.miller@company.com', 'Marketing', 67000.00, '2020-12-03'),
(1008, 'Frank', 'Wilson', 'frank.wilson@company.com', 'Sales', 72000.00, '2021-01-28'),
(1009, 'Grace', 'Moore', 'grace.moore@company.com', 'Engineering', 78000.00, '2020-05-14'),
(1010, 'Henry', 'Taylor', 'henry.taylor@company.com', 'HR', 62000.00, '2020-10-22');

-- Insert sample sales data
INSERT INTO sales VALUES
(2001, 1004, 5001, 'Laptop', 2, 1200.00, '2024-01-15', 'North'),
(2002, 1008, 5002, 'Mouse', 5, 25.00, '2024-01-16', 'South'),
(2003, 1004, 5003, 'Keyboard', 3, 75.00, '2024-01-17', 'North'),
(2004, 1008, 5004, 'Monitor', 1, 350.00, '2024-01-18', 'South'),
(2005, 1004, 5005, 'Laptop', 1, 1200.00, '2024-01-19', 'North'),
(2006, 1008, 5006, 'Tablet', 2, 500.00, '2024-01-20', 'South'),
(2007, 1004, 5007, 'Phone', 3, 800.00, '2024-01-21', 'North'),
(2008, 1008, 5008, 'Headphones', 4, 150.00, '2024-01-22', 'South'),
(2009, 1004, 5009, 'Camera', 1, 600.00, '2024-01-23', 'North'),
(2010, 1008, 5010, 'Printer', 1, 300.00, '2024-01-24', 'South');

-- Insert sample customers data
INSERT INTO customers VALUES
(5001, 'Tech Corp', 'contact@techcorp.com', '555-0101', '123 Business Ave', 'New York', 'NY', '10001', '2023-01-15', 'Business'),
(5002, 'John Consumer', 'john@personal.com', '555-0102', '456 Home St', 'Miami', 'FL', '33101', '2023-02-20', 'Individual'),
(5003, 'Office Solutions', 'orders@officesolutions.com', '555-0103', '789 Corporate Blvd', 'Chicago', 'IL', '60601', '2023-03-10', 'Business'),
(5004, 'Sarah Designer', 'sarah@design.com', '555-0104', '321 Creative Way', 'Los Angeles', 'CA', '90210', '2023-04-05', 'Individual'),
(5005, 'StartupXYZ', 'hello@startupxyz.com', '555-0105', '654 Innovation Dr', 'Austin', 'TX', '73301', '2023-05-12', 'Business');

-- Create tables for export demonstrations
CREATE TABLE IF NOT EXISTS employee_summary (
    department VARCHAR(50),
    employee_count INT,
    avg_salary DECIMAL(10,2),
    max_salary DECIMAL(10,2),
    min_salary DECIMAL(10,2)
);

CREATE TABLE IF NOT EXISTS sales_by_region (
    region VARCHAR(50),
    total_sales INT,
    total_revenue DECIMAL(12,2),
    avg_order_value DECIMAL(10,2)
);

CREATE TABLE IF NOT EXISTS employees_updated (
    employee_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    department VARCHAR(50),
    salary DECIMAL(10,2),
    hire_date DATE,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
