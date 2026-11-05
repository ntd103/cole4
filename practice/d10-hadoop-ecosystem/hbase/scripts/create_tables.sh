#!/bin/bash
# HBase table creation and data loading script

# Start HBase shell and create tables
hbase shell << 'EOF'

# Create employee_profiles table with column families
create 'employee_profiles', 'personal', 'professional', 'contact'

# Create sales_records table
create 'sales_records', 'transaction', 'customer', 'product'

# Create customer_analytics table
create 'customer_analytics', 'demographics', 'behavior', 'preferences'

# List tables to verify creation
list

# Insert sample data into employee_profiles
put 'employee_profiles', '1001', 'personal:first_name', 'John'
put 'employee_profiles', '1001', 'personal:last_name', 'Smith'
put 'employee_profiles', '1001', 'professional:department', 'Engineering'
put 'employee_profiles', '1001', 'professional:salary', '75000'
put 'employee_profiles', '1001', 'professional:hire_date', '2020-01-15'
put 'employee_profiles', '1001', 'contact:email', 'john.smith@company.com'

put 'employee_profiles', '1002', 'personal:first_name', 'Jane'
put 'employee_profiles', '1002', 'personal:last_name', 'Doe'
put 'employee_profiles', '1002', 'professional:department', 'Marketing'
put 'employee_profiles', '1002', 'professional:salary', '65000'
put 'employee_profiles', '1002', 'professional:hire_date', '2020-02-20'
put 'employee_profiles', '1002', 'contact:email', 'jane.doe@company.com'

# Insert sample data into sales_records
put 'sales_records', '2001', 'transaction:sale_id', '2001'
put 'sales_records', '2001', 'transaction:employee_id', '1004'
put 'sales_records', '2001', 'transaction:sale_date', '2024-01-15'
put 'sales_records', '2001', 'transaction:quantity', '2'
put 'sales_records', '2001', 'transaction:unit_price', '1200.00'
put 'sales_records', '2001', 'customer:customer_id', '5001'
put 'sales_records', '2001', 'product:name', 'Laptop'
put 'sales_records', '2001', 'transaction:region', 'North'

put 'sales_records', '2002', 'transaction:sale_id', '2002'
put 'sales_records', '2002', 'transaction:employee_id', '1008'
put 'sales_records', '2002', 'transaction:sale_date', '2024-01-16'
put 'sales_records', '2002', 'transaction:quantity', '5'
put 'sales_records', '2002', 'transaction:unit_price', '25.00'
put 'sales_records', '2002', 'customer:customer_id', '5002'
put 'sales_records', '2002', 'product:name', 'Mouse'
put 'sales_records', '2002', 'transaction:region', 'South'

# Insert sample data into customer_analytics
put 'customer_analytics', '5001', 'demographics:name', 'Tech Corp'
put 'customer_analytics', '5001', 'demographics:type', 'Business'
put 'customer_analytics', '5001', 'demographics:city', 'New York'
put 'customer_analytics', '5001', 'demographics:state', 'NY'
put 'customer_analytics', '5001', 'behavior:registration_date', '2023-01-15'
put 'customer_analytics', '5001', 'behavior:last_purchase', '2024-01-15'
put 'customer_analytics', '5001', 'preferences:preferred_products', 'Laptop,Monitor'

put 'customer_analytics', '5002', 'demographics:name', 'John Consumer'
put 'customer_analytics', '5002', 'demographics:type', 'Individual'
put 'customer_analytics', '5002', 'demographics:city', 'Miami'
put 'customer_analytics', '5002', 'demographics:state', 'FL'
put 'customer_analytics', '5002', 'behavior:registration_date', '2023-02-20'
put 'customer_analytics', '5002', 'behavior:last_purchase', '2024-01-16'
put 'customer_analytics', '5002', 'preferences:preferred_products', 'Mouse,Keyboard'

# Display table descriptions
describe 'employee_profiles'
describe 'sales_records'
describe 'customer_analytics'

EOF

echo "HBase tables created and sample data loaded successfully!"
