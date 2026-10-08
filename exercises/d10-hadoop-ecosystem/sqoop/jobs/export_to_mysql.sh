#!/bin/bash
# Sqoop export jobs from HDFS to MySQL

# Export processed data back to MySQL
sqoop export \
--connect jdbc:mysql://mysql:3306/testdb \
--username sqoop \
--password sqoop \
--table employee_summary \
--export-dir /user/hive/warehouse/employee_summary \
--input-fields-terminated-by ',' \
--num-mappers 1

# Export sales analysis results
sqoop export \
--connect jdbc:mysql://mysql:3306/testdb \
--username sqoop \
--password sqoop \
--table sales_by_region \
--export-dir /user/hive/warehouse/sales_by_region \
--input-fields-terminated-by ',' \
--num-mappers 1

# Export with update mode
sqoop export \
--connect jdbc:mysql://mysql:3306/testdb \
--username sqoop \
--password sqoop \
--table employees_updated \
--export-dir /user/hive/warehouse/employees_processed \
--update-key employee_id \
--update-mode updateonly \
--input-fields-terminated-by ',' \
--num-mappers 1
