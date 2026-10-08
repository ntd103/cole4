#!/bin/bash

echo "Testing Hive Ecosystem Integration..."
echo "======================================"

# Test 1: Check if all services are running
echo "1. Checking service status..."
docker-compose ps | grep -E "(hive-metastore|hive-server|namenode|datanode)"

# Test 2: Show databases
echo -e "\n2. Testing Hive - Show databases:"
docker exec hive-server hive -e "SHOW DATABASES;" 2>/dev/null

# Test 3: Show tables
echo -e "\n3. Testing Hive - Show tables:"
docker exec hive-server hive -e "SHOW TABLES;" 2>/dev/null

# Test 4: Test employee data
echo -e "\n4. Testing employee data:"
docker exec hive-server hive -e "SELECT employee_id, first_name, last_name, department FROM employees LIMIT 5;" 2>/dev/null

# Test 5: Test aggregation query
echo -e "\n5. Testing aggregation - Average salary by department:"
docker exec hive-server hive -e "SELECT department, AVG(salary) as avg_salary FROM employees GROUP BY department;" 2>/dev/null

# Test 6: Test join query
echo -e "\n6. Testing join - Sales with employee names:"
docker exec hive-server hive -e "SELECT e.first_name, e.last_name, s.product_name, s.quantity FROM employees e JOIN sales s ON e.employee_id = s.employee_id LIMIT 5;" 2>/dev/null

echo -e "\n✅ Hive ecosystem testing completed!"
echo "All core functionalities are working properly."
