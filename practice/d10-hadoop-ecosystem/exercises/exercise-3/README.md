# Exercise 3: HBase NoSQL Operations (Intermediate Level)

## Objective
Learn HBase NoSQL database operations including table design, data modeling, CRUD operations, and advanced queries.

## Prerequisites
- Exercises 1 and 2 completed
- HBase Master running at http://localhost:16010
- Understanding of column-family data model

## Tasks

### Task 3.1: Table Design and Creation (25 points)
Design and create HBase tables with appropriate column families.

**Connect to HBase:**
```bash
# Access HBase master container
docker exec -it hbase-master bash

# Start HBase shell
hbase shell
```

**HBase Commands:**
```ruby
# Check HBase status
status

# Create employee profiles table
create 'employee_profiles', 
  {NAME => 'personal', VERSIONS => 3}, 
  {NAME => 'professional', VERSIONS => 5}, 
  {NAME => 'contact', VERSIONS => 1}

# Create sales analytics table
create 'sales_analytics', 
  {NAME => 'transaction', VERSIONS => 1}, 
  {NAME => 'metrics', VERSIONS => 10, TTL => 7776000}

# Create customer behavior table with different settings
create 'customer_behavior', 
  {NAME => 'demographics', COMPRESSION => 'GZ'}, 
  {NAME => 'activity', IN_MEMORY => true}, 
  {NAME => 'preferences', BLOCKCACHE => true}

# List all tables
list

# Describe table structure
describe 'employee_profiles'
describe 'sales_analytics'
describe 'customer_behavior'
```

**Deliverable:**
- Screenshot of table creation and descriptions
- Document explaining your column family design decisions

### Task 3.2: Data Loading and CRUD Operations (30 points)
Perform Create, Read, Update, and Delete operations on HBase tables.

**Data Loading Commands:**
```ruby
# Load employee data
put 'employee_profiles', '1001', 'personal:first_name', 'John'
put 'employee_profiles', '1001', 'personal:last_name', 'Smith'
put 'employee_profiles', '1001', 'personal:birth_date', '1985-03-15'
put 'employee_profiles', '1001', 'professional:department', 'Engineering'
put 'employee_profiles', '1001', 'professional:title', 'Senior Developer'
put 'employee_profiles', '1001', 'professional:salary', '75000'
put 'employee_profiles', '1001', 'professional:start_date', '2020-01-15'
put 'employee_profiles', '1001', 'contact:email', 'john.smith@company.com'
put 'employee_profiles', '1001', 'contact:phone', '555-0101'

# Load more employees (create at least 5 employee records)
put 'employee_profiles', '1002', 'personal:first_name', 'Jane'
put 'employee_profiles', '1002', 'personal:last_name', 'Doe'
put 'employee_profiles', '1002', 'professional:department', 'Marketing'
put 'employee_profiles', '1002', 'professional:salary', '65000'
put 'employee_profiles', '1002', 'contact:email', 'jane.doe@company.com'

# Add more records for employees 1003, 1004, 1005...

# Load sales analytics data
put 'sales_analytics', 'daily_2024_01_15', 'transaction:total_sales', '5'
put 'sales_analytics', 'daily_2024_01_15', 'transaction:total_revenue', '3275.00'
put 'sales_analytics', 'daily_2024_01_15', 'metrics:avg_order_value', '655.00'
put 'sales_analytics', 'daily_2024_01_15', 'metrics:top_product', 'Laptop'
put 'sales_analytics', 'daily_2024_01_15', 'metrics:peak_hour', '14:00'

# Load customer behavior data
put 'customer_behavior', '5001', 'demographics:name', 'Tech Corp'
put 'customer_behavior', '5001', 'demographics:type', 'Business'
put 'customer_behavior', '5001', 'demographics:location', 'New York'
put 'customer_behavior', '5001', 'activity:last_login', '2024-01-15 10:30:00'
put 'customer_behavior', '5001', 'activity:page_views', '25'
put 'customer_behavior', '5001', 'preferences:product_category', 'Electronics'
```

**Read Operations:**
```ruby
# Get specific row
get 'employee_profiles', '1001'

# Get specific column family
get 'employee_profiles', '1001', 'professional'

# Get specific column
get 'employee_profiles', '1001', 'professional:salary'

# Get with timestamp
get 'employee_profiles', '1001', {TIMERANGE => [0, 1234567890000]}
```

**Update Operations:**
```ruby
# Update salary (creates new version)
put 'employee_profiles', '1001', 'professional:salary', '80000'

# Update multiple fields
put 'employee_profiles', '1001', 'professional:title', 'Lead Developer'
put 'employee_profiles', '1001', 'contact:phone', '555-0102'

# Verify updates
get 'employee_profiles', '1001', 'professional:salary'
get 'employee_profiles', '1001', {COLUMN => 'professional:salary', VERSIONS => 3}
```

**Delete Operations:**
```ruby
# Delete specific column
delete 'employee_profiles', '1001', 'contact:phone'

# Delete column family
deleteall 'employee_profiles', '1001', 'contact'

# Verify deletions
get 'employee_profiles', '1001'
```

**Deliverable:**
- Script file with all HBase commands executed
- Screenshots showing data before and after updates/deletes

### Task 3.3: Advanced Querying and Scanning (25 points)
Perform advanced queries using scan operations and filters.

**Scanning Operations:**
```ruby
# Scan entire table
scan 'employee_profiles'

# Scan with column family filter
scan 'employee_profiles', {COLUMNS => 'personal'}

# Scan with row key range
scan 'employee_profiles', {STARTROW => '1000', ENDROW => '1010'}

# Scan with limit
scan 'employee_profiles', {LIMIT => 3}

# Scan with specific columns
scan 'employee_profiles', {COLUMNS => ['personal:first_name', 'professional:department']}
```

**Filter Operations:**
```ruby
# Single column value filter
scan 'employee_profiles', {FILTER => "SingleColumnValueFilter('professional', 'department', =, 'Engineering')"}

# Row key filter
scan 'employee_profiles', {FILTER => "PrefixFilter('100')"}

# Value filter
scan 'employee_profiles', {FILTER => "ValueFilter(=,'substring:John')"}

# Multiple filters with FilterList
scan 'employee_profiles', {FILTER => "FilterList(MUST_PASS_ALL, SingleColumnValueFilter('professional', 'department', =, 'Engineering'), ValueFilter(=,'substring:75000'))"}

# Time-based filter
scan 'employee_profiles', {TIMERANGE => [1609459200000, 1640995200000]}
```

**Analytical Queries:**
```ruby
# Count rows in table
count 'employee_profiles'

# Count rows with filter
count 'employee_profiles', {FILTER => "SingleColumnValueFilter('professional', 'department', =, 'Engineering')"}

# Scan sales analytics for reporting
scan 'sales_analytics'

# Get customer behavior patterns
scan 'customer_behavior', {COLUMNS => 'activity'}
```

**Deliverable:**
- Output files showing results of all scan operations
- Analysis document explaining the query results

### Task 3.4: Row Key Design and Performance (20 points)
Analyze and optimize row key design for performance.

**Row Key Analysis:**
```ruby
# Create a new table with optimized row key design
create 'sales_optimized', 'data'

# Load data with different row key strategies
# Strategy 1: timestamp-based (can cause hotspotting)
put 'sales_optimized', '20240115_001', 'data:product', 'Laptop'
put 'sales_optimized', '20240115_002', 'data:product', 'Mouse'

# Strategy 2: hash prefix to distribute load
put 'sales_optimized', '001_20240115_001', 'data:product', 'Laptop'
put 'sales_optimized', '002_20240115_002', 'data:product', 'Mouse'

# Strategy 3: reverse timestamp for recent data access
put 'sales_optimized', '0000000000_20240115_001', 'data:product', 'Laptop'

# Compare scan performance
scan 'sales_optimized'

# Analyze table regions
# Note: This requires administrative access
```

**Performance Testing:**
```ruby
# Create test data for performance analysis
# Create 100 records with different row key patterns

# Pattern 1: Sequential keys
for i in 1..50
  put 'sales_optimized', sprintf('%03d_sequential', i), 'data:type', 'sequential'
end

# Pattern 2: Random hash prefix
for i in 1..50
  hash_prefix = (i * 31) % 1000
  put 'sales_optimized', sprintf('%03d_random_%03d', hash_prefix, i), 'data:type', 'random'
end

# Compare scan times (note execution time)
scan 'sales_optimized', {FILTER => "SingleColumnValueFilter('data', 'type', =, 'sequential')"}
scan 'sales_optimized', {FILTER => "SingleColumnValueFilter('data', 'type', =, 'random')"}
```

**Deliverable:**
- Performance comparison report
- Row key design recommendations document

## Advanced Challenges (Bonus - 10 points)

### Challenge 1: Bulk Loading
Create a script to bulk load data into HBase tables:

```bash
# Create CSV files for bulk loading
# Use HBase bulk load utilities
```

### Challenge 2: Coprocessors Simulation
Implement server-side processing logic:

```ruby
# Simulate coprocessor functionality with scan and aggregation
# Calculate department-wise salary statistics using scans
```

## Submission Requirements

Create a folder named `exercise3_[your_name]` containing:

1. **hbase_scripts/** folder with all HBase shell commands
2. **outputs/** folder with command results and screenshots
3. **design_document.md** - Column family design explanation (minimum 400 words)
4. **performance_analysis.md** - Row key design and performance analysis (minimum 300 words)
5. **query_analysis.md** - Analysis of scan and filter operations (minimum 300 words)
6. **reflection.md** - Learning outcomes and NoSQL vs SQL comparison (minimum 250 words)

## Grading Rubric

| Component | Points | Criteria |
|-----------|---------|----------|
| Task 3.1 | 25 | Tables created with appropriate column families |
| Task 3.2 | 30 | CRUD operations performed correctly |
| Task 3.3 | 25 | Advanced queries and filters working |
| Task 3.4 | 20 | Row key design analysis completed |
| Bonus | 10 | Advanced challenges attempted |
| **Total** | **110** | |

## Key Concepts to Understand

1. **Column Families**: Grouping related data together
2. **Row Key Design**: Critical for query performance
3. **Versioning**: Handling multiple versions of data
4. **Filters**: Efficient data retrieval patterns
5. **Scanning**: Bulk data access patterns

## Common Issues and Solutions

1. **RegionServer Issues**: Check HBase logs and restart if needed
2. **Memory Problems**: Increase container memory allocation
3. **Row Key Hotspotting**: Use hash prefixes or salting
4. **Slow Scans**: Optimize filters and row key design

## Performance Tips

1. **Row Key Design**: Avoid monotonically increasing keys
2. **Column Family Count**: Keep to minimum (2-3 families max)
3. **Filter Usage**: Push filters to server side
4. **Batch Operations**: Use batch puts for bulk loading

## Additional Resources
- [HBase Reference Guide](https://hbase.apache.org/book.html)
- [HBase Row Key Design](https://hbase.apache.org/book.html#rowkey.design)
- [HBase Performance Tuning](https://hbase.apache.org/book.html#performance)
