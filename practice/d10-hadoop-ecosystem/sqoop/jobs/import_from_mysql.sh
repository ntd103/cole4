#!/bin/bash
# Sqoop import jobs from MySQL to HDFS

# Import entire employees table
sqoop import \
--connect jdbc:mysql://mysql:3306/testdb \
--username sqoop \
--password sqoop \
--table employees \
--target-dir /user/sqoop/employees \
--num-mappers 1 \
--fields-terminated-by ',' \
--lines-terminated-by '\n'

# Import sales table with specific columns
sqoop import \
--connect jdbc:mysql://mysql:3306/testdb \
--username sqoop \
--password sqoop \
--table sales \
--columns "sale_id,employee_id,customer_id,product_name,quantity,unit_price,sale_date" \
--target-dir /user/sqoop/sales \
--num-mappers 1 \
--fields-terminated-by ','

# Import with WHERE clause (filtering)
sqoop import \
--connect jdbc:mysql://mysql:3306/testdb \
--username sqoop \
--password sqoop \
--table employees \
--where "department='Engineering'" \
--target-dir /user/sqoop/engineering_employees \
--num-mappers 1 \
--fields-terminated-by ','

# Import as Parquet format
sqoop import \
--connect jdbc:mysql://mysql:3306/testdb \
--username sqoop \
--password sqoop \
--table sales \
--target-dir /user/sqoop/sales_parquet \
--as-parquetfile \
--num-mappers 1

# Incremental import (append mode)
sqoop import \
--connect jdbc:mysql://mysql:3306/testdb \
--username sqoop \
--password sqoop \
--table sales \
--target-dir /user/sqoop/sales_incremental \
--incremental append \
--check-column sale_id \
--last-value 0 \
--num-mappers 1
