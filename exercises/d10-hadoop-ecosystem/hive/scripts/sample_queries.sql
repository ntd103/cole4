-- Sample queries for Hive demonstration

-- 1. Basic SELECT with filtering
SELECT employee_id, first_name, last_name, department, salary
FROM employees
WHERE department = 'Engineering'
ORDER BY salary DESC;

-- 2. Aggregation by department
SELECT department, 
       COUNT(*) as employee_count,
       AVG(salary) as avg_salary,
       MAX(salary) as max_salary,
       MIN(salary) as min_salary
FROM employees
GROUP BY department
ORDER BY avg_salary DESC;

-- 3. Join between employees and sales
SELECT e.first_name, e.last_name, e.department,
       COUNT(s.sale_id) as total_sales,
       SUM(s.quantity * s.unit_price) as total_revenue
FROM employees e
LEFT JOIN sales s ON e.employee_id = s.employee_id
GROUP BY e.employee_id, e.first_name, e.last_name, e.department
ORDER BY total_revenue DESC;

-- 4. Sales by region and month
SELECT region,
       YEAR(sale_date) as sale_year,
       MONTH(sale_date) as sale_month,
       COUNT(*) as num_sales,
       SUM(quantity * unit_price) as total_revenue
FROM sales
GROUP BY region, YEAR(sale_date), MONTH(sale_date)
ORDER BY sale_year, sale_month, region;

-- 5. Top selling products
SELECT product_name,
       SUM(quantity) as total_quantity,
       SUM(quantity * unit_price) as total_revenue,
       AVG(unit_price) as avg_price
FROM sales
GROUP BY product_name
ORDER BY total_revenue DESC
LIMIT 5;
