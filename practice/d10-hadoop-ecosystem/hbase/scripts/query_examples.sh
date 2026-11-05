#!/bin/bash
# HBase query examples

hbase shell << 'EOF'

# Basic operations
echo "=== Basic HBase Operations ==="

# 1. Get specific row
echo "Getting employee 1001 profile:"
get 'employee_profiles', '1001'

# 2. Get specific column family
echo "Getting professional info for employee 1001:"
get 'employee_profiles', '1001', 'professional'

# 3. Get specific column
echo "Getting salary for employee 1001:"
get 'employee_profiles', '1001', 'professional:salary'

# 4. Scan entire table
echo "Scanning employee_profiles table:"
scan 'employee_profiles'

# 5. Scan with column family filter
echo "Scanning only personal information:"
scan 'employee_profiles', {COLUMNS => 'personal'}

# 6. Scan with row key filter
echo "Scanning employees starting with '100':"
scan 'employee_profiles', {STARTROW => '1000', ENDROW => '1010'}

# 7. Count rows in table
echo "Counting rows in employee_profiles:"
count 'employee_profiles'

# Advanced operations
echo "=== Advanced HBase Operations ==="

# 8. Update existing data
echo "Updating employee 1001 salary:"
put 'employee_profiles', '1001', 'professional:salary', '80000'

# 9. Add new column
echo "Adding performance rating:"
put 'employee_profiles', '1001', 'professional:rating', 'Excellent'

# 10. Delete specific column
echo "Deleting old salary value:"
delete 'employee_profiles', '1001', 'professional:salary'

# 11. Scan sales records
echo "Scanning sales records:"
scan 'sales_records'

# 12. Get customer analytics
echo "Getting customer analytics for customer 5001:"
get 'customer_analytics', '5001'

EOF
