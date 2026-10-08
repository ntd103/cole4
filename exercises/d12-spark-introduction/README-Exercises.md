# Apache Spark Progressive Exercises

## Getting Started Instructions

1. **Environment Setup**:
   ```bash
   # Clone or download the demo materials
   # Navigate to the project directory
   cd spark-demo
   
   # Generate sample data
   python3 scripts/generate_sample_data.py
   
   # Start the Spark cluster
   docker-compose up -d
   
   # Wait for services to start (about 30 seconds)
   # Access Jupyter Lab: http://localhost:8889
   ```

2. **Verify Setup**:
   - Spark Master UI: http://localhost:8080
   - Jupyter Lab: http://localhost:8889 (password: `jupyter`)
   - Ensure you can see 2 worker nodes in the Master UI

---

## Exercise 1: Spark Fundamentals (Beginner)
**Estimated time: 30-45 minutes**

### Learning Goals:
- Understand RDD operations
- Practice transformations vs actions
- Learn about lazy evaluation

### Tasks:

#### Task 1.1: RDD Basics
```python
# Create a Spark session
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Exercise1") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

sc = spark.sparkContext

# TODO: Create an RDD from the range 1 to 1000
numbers = sc.parallelize(range(1, 1001))

# TODO: Filter for numbers divisible by 7
divisible_by_7 = numbers.filter(lambda x: x % 7 == 0)

# TODO: Square each number
squared = divisible_by_7.map(lambda x: x ** 2)

# TODO: Find the count, sum, and average
count = squared.count()
total = squared.sum()
average = total / count

print(f"Count: {count}")
print(f"Sum: {total}")
print(f"Average: {average}")
```

#### Task 1.2: Text Processing with RDDs
```python
# TODO: Create an RDD from this text
text = ["Apache Spark is a unified analytics engine",
        "for large-scale data processing",
        "Spark provides high-level APIs in Java, Scala, Python and R",
        "and supports SQL, streaming, machine learning and graph processing"]

text_rdd = sc.parallelize(text)

# TODO: Split each line into words and flatten
words = text_rdd.flatMap(lambda line: line.split())

# TODO: Convert to lowercase and remove punctuation
clean_words = words.map(lambda word: word.lower().replace(",", "").replace(".", ""))

# TODO: Count occurrences of each word
word_counts = clean_words.map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)

# TODO: Sort by count in descending order and collect top 10
top_words = word_counts.sortBy(lambda x: x[1], ascending=False).take(10)

print("Top 10 most frequent words:")
for word, count in top_words:
    print(f"{word}: {count}")
```

#### Task 1.3: Understanding Partitions
```python
# TODO: Create an RDD and check its partitions
data = sc.parallelize(range(1, 101))
print(f"Original partitions: {data.getNumPartitions()}")

# TODO: Repartition to 4 partitions
repartitioned = data.repartition(4)
print(f"After repartitioning: {repartitioned.getNumPartitions()}")

# TODO: Show data distribution across partitions
def show_partition_contents(iterator):
    yield f"Partition contains: {list(iterator)}"

partition_contents = repartitioned.mapPartitions(show_partition_contents).collect()
for i, content in enumerate(partition_contents):
    print(f"Partition {i}: {len(eval(content.split(': ')[1]))} elements")
```

**Expected Output**: Students should see word counts, understand partition distribution, and observe lazy evaluation.

---

## Exercise 2: DataFrame Operations (Beginner-Intermediate)
**Estimated time: 45-60 minutes**

### Learning Goals:
- Master DataFrame API
- Understand schema and data types
- Practice aggregations and joins

### Tasks:

#### Task 2.1: Data Exploration
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

spark = SparkSession.builder.appName("Exercise2").getOrCreate()

# TODO: Load the sales data
sales_df = spark.read.csv("/home/jovyan/data/csv/sales_data.csv", header=True, inferSchema=True)

# TODO: Display basic information
print(f"Number of rows: {sales_df.count()}")
print(f"Number of columns: {len(sales_df.columns)}")
print("\nSchema:")
sales_df.printSchema()

# TODO: Show first 10 rows
sales_df.show(10)

# TODO: Get summary statistics for numeric columns
sales_df.describe().show()
```

#### Task 2.2: Data Analysis Questions
**Answer these questions using DataFrame operations:**

1. **What is the total revenue by region?**
```python
# TODO: Group by region and sum total_amount
region_revenue = sales_df.groupBy("region").agg(sum("total_amount").alias("total_revenue"))
region_revenue.orderBy(desc("total_revenue")).show()
```

2. **Which product category has the highest average order value?**
```python
# TODO: Group by category and calculate average total_amount
category_avg = sales_df.groupBy("category").agg(avg("total_amount").alias("avg_order_value"))
category_avg.orderBy(desc("avg_order_value")).show()
```

3. **What are the top 5 customers by total spending?**
```python
# TODO: Group by customer_id and sum total_amount
top_customers = sales_df.groupBy("customer_id").agg(sum("total_amount").alias("total_spent"))
top_customers.orderBy(desc("total_spent")).show(5)
```

4. **Create a monthly sales trend**
```python
# TODO: Extract year-month from date and aggregate
monthly_sales = sales_df \
    .withColumn("year_month", date_format("date", "yyyy-MM")) \
    .groupBy("year_month") \
    .agg(sum("total_amount").alias("monthly_revenue")) \
    .orderBy("year_month")

monthly_sales.show()
```

#### Task 2.3: Advanced Transformations
```python
# TODO: Create customer segments based on spending
customer_segments = sales_df \
    .groupBy("customer_id") \
    .agg(sum("total_amount").alias("total_spent")) \
    .withColumn("segment", 
                when(col("total_spent") >= 5000, "VIP")
                .when(col("total_spent") >= 2000, "Premium")
                .when(col("total_spent") >= 500, "Regular")
                .otherwise("Basic"))

# TODO: Count customers in each segment
segment_counts = customer_segments.groupBy("segment").count()
segment_counts.show()

# TODO: Add a profit margin calculation
# (Assume 20% profit margin)
sales_with_profit = sales_df.withColumn("profit", col("total_amount") * 0.2)

# TODO: Show top 10 most profitable transactions
sales_with_profit.orderBy(desc("profit")).select("transaction_id", "category", "total_amount", "profit").show(10)
```

**Expected Output**: Students should produce meaningful business insights from the data.

---

## Exercise 3: Spark SQL and Joins (Intermediate)
**Estimated time: 60-75 minutes**

### Learning Goals:
- Master Spark SQL syntax
- Understand different join types
- Practice complex analytical queries

### Tasks:

#### Task 3.1: SQL Setup and Basic Queries
```python
# Load all datasets
sales_df = spark.read.csv("/home/jovyan/data/csv/sales_data.csv", header=True, inferSchema=True)
customers_df = spark.read.csv("/home/jovyan/data/csv/customers.csv", header=True, inferSchema=True)
products_df = spark.read.csv("/home/jovyan/data/csv/products.csv", header=True, inferSchema=True)

# TODO: Create temporary views
sales_df.createOrReplaceTempView("sales")
customers_df.createOrReplaceTempView("customers")
products_df.createOrReplaceTempView("products")

# TODO: Write SQL to find total sales by loyalty tier
loyalty_sales_sql = """
SELECT 
    c.loyalty_tier,
    COUNT(*) as transaction_count,
    SUM(s.total_amount) as total_revenue,
    AVG(s.total_amount) as avg_order_value
FROM sales s
JOIN customers c ON s.customer_id = c.customer_id
GROUP BY c.loyalty_tier
ORDER BY total_revenue DESC
"""

spark.sql(loyalty_sales_sql).show()
```

#### Task 3.2: Complex Analytics Queries

**Query 1: Customer Lifetime Value Analysis**
```sql
-- TODO: Write a query to calculate customer lifetime value by age group
SELECT 
    CASE 
        WHEN c.age < 30 THEN 'Young (18-29)'
        WHEN c.age < 45 THEN 'Middle (30-44)'
        WHEN c.age < 60 THEN 'Mature (45-59)'
        ELSE 'Senior (60+)'
    END as age_group,
    c.loyalty_tier,
    COUNT(DISTINCT s.customer_id) as customer_count,
    SUM(s.total_amount) as total_revenue,
    AVG(s.total_amount) as avg_order_value,
    SUM(s.total_amount) / COUNT(DISTINCT s.customer_id) as avg_lifetime_value
FROM sales s
JOIN customers c ON s.customer_id = c.customer_id
GROUP BY age_group, c.loyalty_tier
ORDER BY age_group, total_revenue DESC
```

**Query 2: Product Performance Analysis**
```sql
-- TODO: Analyze product performance with profit margins
SELECT 
    p.category,
    p.product_name,
    COUNT(*) as times_sold,
    SUM(s.quantity) as total_quantity,
    SUM(s.total_amount) as total_revenue,
    SUM(s.quantity * p.cost_price) as total_cost,
    SUM(s.total_amount) - SUM(s.quantity * p.cost_price) as total_profit,
    AVG(p.profit_margin) as avg_margin
FROM sales s
JOIN products p ON s.category = p.category AND s.product_name = p.product_name
GROUP BY p.category, p.product_name
HAVING COUNT(*) >= 10  -- Only products sold at least 10 times
ORDER BY total_profit DESC
```

**Query 3: Seasonal Analysis with Window Functions**
```sql
-- TODO: Use window functions to analyze seasonal trends
SELECT 
    EXTRACT(MONTH FROM date) as month,
    EXTRACT(YEAR FROM date) as year,
    category,
    SUM(total_amount) as monthly_sales,
    LAG(SUM(total_amount)) OVER (PARTITION BY category ORDER BY EXTRACT(YEAR FROM date), EXTRACT(MONTH FROM date)) as prev_month_sales,
    SUM(total_amount) - LAG(SUM(total_amount)) OVER (PARTITION BY category ORDER BY EXTRACT(YEAR FROM date), EXTRACT(MONTH FROM date)) as month_over_month_change
FROM sales
GROUP BY EXTRACT(YEAR FROM date), EXTRACT(MONTH FROM date), category
ORDER BY year, month, category
```

#### Task 3.3: Join Practice
```python
# TODO: Practice different join types

# Inner join: Sales with customer details
inner_join = sales_df.join(customers_df, "customer_id", "inner")
print(f"Inner join count: {inner_join.count()}")

# Left join: All sales, with customer details where available
left_join = sales_df.join(customers_df, "customer_id", "left")
print(f"Left join count: {left_join.count()}")

# Broadcast join: For small datasets (products)
from pyspark.sql.functions import broadcast
broadcast_join = sales_df.join(broadcast(products_df), ["category", "product_name"], "left")
broadcast_join.explain()  # Check execution plan

# Self join: Find customers who bought the same product
same_product = sales_df.alias("s1").join(
    sales_df.alias("s2"), 
    (col("s1.product_name") == col("s2.product_name")) & 
    (col("s1.customer_id") != col("s2.customer_id"))
).select("s1.customer_id", "s2.customer_id", "s1.product_name").distinct()

same_product.show(10)
```

**Expected Output**: Complex analytical insights combining multiple datasets.

---

## Exercise 4: Performance Optimization (Intermediate-Advanced)
**Estimated time: 60-90 minutes**

### Learning Goals:
- Understand Spark performance concepts
- Practice optimization techniques
- Learn monitoring and debugging

### Tasks:

#### Task 4.1: Partitioning Optimization
```python
import time
from pyspark.sql.functions import *

# Load large dataset
sales_df = spark.read.csv("/home/jovyan/data/csv/sales_data.csv", header=True, inferSchema=True)

# TODO: Analyze current partitioning
print(f"Current partitions: {sales_df.rdd.getNumPartitions()}")
print(f"Estimated partition size: {sales_df.count() / sales_df.rdd.getNumPartitions()} rows per partition")

# TODO: Time a groupBy operation with current partitioning
start_time = time.time()
result1 = sales_df.groupBy("region").agg(sum("total_amount")).collect()
time1 = time.time() - start_time

# TODO: Repartition by region and time the same operation
repartitioned_df = sales_df.repartition("region")
start_time = time.time()
result2 = repartitioned_df.groupBy("region").agg(sum("total_amount")).collect()
time2 = time.time() - start_time

print(f"Original partitioning time: {time1:.2f} seconds")
print(f"Optimized partitioning time: {time2:.2f} seconds")
print(f"Improvement: {((time1 - time2) / time1) * 100:.1f}%")
```

#### Task 4.2: Caching Strategy
```python
# TODO: Demonstrate caching benefits
customers_df = spark.read.csv("/home/jovyan/data/csv/customers.csv", header=True, inferSchema=True)

# Complex transformation that will be reused
complex_customer_data = customers_df \
    .withColumn("age_group", 
                when(col("age") < 30, "Young")
                .when(col("age") < 50, "Middle")
                .otherwise("Senior")) \
    .withColumn("signup_year", year(to_date("signup_date"))) \
    .filter(col("loyalty_tier").isin(["Gold", "Platinum"]))

# TODO: Time without caching
start_time = time.time()
count1 = complex_customer_data.count()
analysis1 = complex_customer_data.groupBy("age_group").count().collect()
time_without_cache = time.time() - start_time

# TODO: Cache and time with caching
complex_customer_data.cache()
start_time = time.time()
count2 = complex_customer_data.count()
analysis2 = complex_customer_data.groupBy("age_group").count().collect()
time_with_cache = time.time() - start_time

print(f"Without cache: {time_without_cache:.2f} seconds")
print(f"With cache: {time_with_cache:.2f} seconds")
print(f"Cache improvement: {((time_without_cache - time_with_cache) / time_without_cache) * 100:.1f}%")
```

#### Task 4.3: Query Optimization
```python
# TODO: Compare different approaches to the same problem

# Approach 1: Multiple passes over data
start_time = time.time()
total_sales = sales_df.agg(sum("total_amount")).collect()[0][0]
avg_sales = sales_df.agg(avg("total_amount")).collect()[0][0]
max_sales = sales_df.agg(max("total_amount")).collect()[0][0]
approach1_time = time.time() - start_time

# Approach 2: Single pass with multiple aggregations
start_time = time.time()
all_stats = sales_df.agg(
    sum("total_amount").alias("total"),
    avg("total_amount").alias("average"),
    max("total_amount").alias("maximum")
).collect()[0]
approach2_time = time.time() - start_time

print(f"Multiple passes: {approach1_time:.2f} seconds")
print(f"Single pass: {approach2_time:.2f} seconds")
print(f"Single pass is {approach1_time/approach2_time:.1f}x faster")

# TODO: Analyze shuffle operations
# Bad: Multiple shuffles
bad_query = sales_df \
    .groupBy("region").agg(sum("total_amount").alias("region_total")) \
    .join(sales_df.groupBy("category").agg(sum("total_amount").alias("category_total")), 
          sales_df.region == sales_df.category)  # This join doesn't make sense but shows multiple shuffles

# Good: Minimize shuffles
good_query = sales_df \
    .groupBy("region", "category") \
    .agg(sum("total_amount").alias("total")) \
    .withColumn("region_total", sum("total").over(Window.partitionBy("region"))) \
    .withColumn("category_total", sum("total").over(Window.partitionBy("category")))

print("Bad query plan:")
bad_query.explain()
print("\nGood query plan:")
good_query.explain()
```

#### Task 4.4: Memory Management
```python
# TODO: Monitor memory usage and storage levels
from pyspark import StorageLevel

# Create a large DataFrame for testing
large_df = sales_df.repartition(8).cache()
large_df.count()  # Materialize cache

# Check cache usage
print("Storage Level:", large_df.storageLevel)

# Try different storage levels
memory_only = sales_df.repartition(4)
memory_only.persist(StorageLevel.MEMORY_ONLY)

memory_and_disk = sales_df.repartition(4)
memory_and_disk.persist(StorageLevel.MEMORY_AND_DISK)

serialized = sales_df.repartition(4)
serialized.persist(StorageLevel.MEMORY_ONLY_SER)

# TODO: Test performance with different storage levels
def test_storage_performance(df, name):
    start_time = time.time()
    count = df.count()
    df.groupBy("category").count().collect()
    end_time = time.time()
    print(f"{name}: {end_time - start_time:.2f} seconds")

test_storage_performance(memory_only, "MEMORY_ONLY")
test_storage_performance(memory_and_disk, "MEMORY_AND_DISK")
test_storage_performance(serialized, "MEMORY_ONLY_SER")

# Clean up
spark.catalog.clearCache()
```

**Expected Output**: Students should see measurable performance improvements and understand the trade-offs.

---

## Exercise 5: Real-World Data Pipeline (Advanced)
**Estimated time: 90-120 minutes**

### Learning Goals:
- Build end-to-end data pipeline
- Handle data quality issues
- Implement business logic
- Create reusable functions

### Tasks:

#### Task 5.1: Data Quality Assessment
```python
from pyspark.sql.functions import *
from pyspark.sql.types import *

def assess_data_quality(df, table_name):
    """Comprehensive data quality assessment"""
    print(f"\n=== Data Quality Report for {table_name} ===")
    
    # Basic statistics
    total_rows = df.count()
    total_cols = len(df.columns)
    print(f"Total rows: {total_rows:,}")
    print(f"Total columns: {total_cols}")
    
    # Check for nulls in each column
    print("\nNull value analysis:")
    null_counts = df.select([count(when(col(c).isNull(), c)).alias(c) for c in df.columns])
    null_summary = null_counts.collect()[0].asDict()
    
    for column, null_count in null_summary.items():
        null_percentage = (null_count / total_rows) * 100
        if null_count > 0:
            print(f"  {column}: {null_count} nulls ({null_percentage:.1f}%)")
    
    # Check for duplicates
    distinct_rows = df.distinct().count()
    duplicates = total_rows - distinct_rows
    if duplicates > 0:
        print(f"\nDuplicate rows: {duplicates} ({(duplicates/total_rows)*100:.1f}%)")
    else:
        print("\nNo duplicate rows found")
    
    # Data type analysis
    print(f"\nData types:")
    for field in df.schema.fields:
        print(f"  {field.name}: {field.dataType}")
    
    return {
        'total_rows': total_rows,
        'null_summary': null_summary,
        'duplicates': duplicates,
        'distinct_rows': distinct_rows
    }

# TODO: Assess quality of all datasets
sales_df = spark.read.csv("/home/jovyan/data/csv/sales_data.csv", header=True, inferSchema=True)
customers_df = spark.read.csv("/home/jovyan/data/csv/customers.csv", header=True, inferSchema=True)
products_df = spark.read.csv("/home/jovyan/data/csv/products.csv", header=True, inferSchema=True)

sales_quality = assess_data_quality(sales_df, "Sales")
customer_quality = assess_data_quality(customers_df, "Customers")
product_quality = assess_data_quality(products_df, "Products")
```

#### Task 5.2: Data Cleaning and Transformation Pipeline
```python
def clean_sales_data(sales_df):
    """Clean and standardize sales data"""
    print("Cleaning sales data...")
    
    # Remove invalid transactions (negative amounts, zero quantities)
    cleaned_df = sales_df.filter(
        (col("total_amount") > 0) & 
        (col("quantity") > 0) &
        (col("unit_price") > 0)
    )
    
    # Standardize region names
    cleaned_df = cleaned_df.withColumn("region", 
        when(col("region").isin(["north", "North", "NORTH"]), "North")
        .when(col("region").isin(["south", "South", "SOUTH"]), "South")
        .when(col("region").isin(["east", "East", "EAST"]), "East")
        .when(col("region").isin(["west", "West", "WEST"]), "West")
        .when(col("region").isin(["central", "Central", "CENTRAL"]), "Central")
        .otherwise(col("region"))
    )
    
    # Add derived columns
    cleaned_df = cleaned_df \
        .withColumn("date_formatted", to_date("date")) \
        .withColumn("year", year(to_date("date"))) \
        .withColumn("month", month(to_date("date"))) \
        .withColumn("quarter", quarter(to_date("date"))) \
        .withColumn("day_of_week", dayofweek(to_date("date"))) \
        .withColumn("is_weekend", col("day_of_week").isin([1, 7]).cast("boolean")) \
        .withColumn("revenue_per_unit", round(col("total_amount") / col("quantity"), 2))
    
    # Validate calculations
    validation_df = cleaned_df.withColumn("calculated_total", 
        round(col("quantity") * col("unit_price"), 2))
    
    # Check for calculation discrepancies
    discrepancies = validation_df.filter(
        abs(col("total_amount") - col("calculated_total")) > 0.01
    ).count()
    
    if discrepancies > 0:
        print(f"Warning: {discrepancies} transactions have calculation discrepancies")
    
    return cleaned_df.drop("calculated_total")

def enrich_customer_data(customers_df):
    """Enrich customer data with additional features"""
    print("Enriching customer data...")
    
    enriched_df = customers_df \
        .withColumn("signup_date_formatted", to_date("signup_date")) \
        .withColumn("account_age_days", 
            datediff(current_date(), to_date("signup_date"))) \
        .withColumn("account_age_years", 
            round(col("account_age_days") / 365.25, 1)) \
        .withColumn("generation",
            when(col("age") < 25, "Gen Z")
            .when(col("age") < 40, "Millennial") 
            .when(col("age") < 55, "Gen X")
            .otherwise("Boomer")) \
        .withColumn("loyalty_tier_numeric",
            when(col("loyalty_tier") == "Bronze", 1)
            .when(col("loyalty_tier") == "Silver", 2)
            .when(col("loyalty_tier") == "Gold", 3)
            .when(col("loyalty_tier") == "Platinum", 4)
            .otherwise(0))
    
    return enriched_df

# TODO: Apply cleaning functions
clean_sales = clean_sales_data(sales_df)
enriched_customers = enrich_customer_data(customers_df)

print(f"Original sales records: {sales_df.count()}")
print(f"Cleaned sales records: {clean_sales.count()}")
print(f"Records removed: {sales_df.count() - clean_sales.count()}")
```

#### Task 5.3: Advanced Analytics Pipeline
```python
def calculate_customer_metrics(sales_df, customers_df):
    """Calculate comprehensive customer metrics"""
    print("Calculating customer metrics...")
    
    # Customer transaction metrics
    customer_metrics = sales_df.groupBy("customer_id").agg(
        count("*").alias("transaction_count"),
        sum("total_amount").alias("total_lifetime_value"),
        avg("total_amount").alias("avg_order_value"),
        min("date_formatted").alias("first_purchase_date"),
        max("date_formatted").alias("last_purchase_date"),
        countDistinct("category").alias("category_diversity"),
        countDistinct("product_name").alias("product_diversity"),
        stddev("total_amount").alias("order_value_std")
    )
    
    # Calculate recency, frequency, monetary (RFM)
    current_date = sales_df.agg(max("date_formatted")).collect()[0][0]
    
    rfm_metrics = customer_metrics \
        .withColumn("recency_days", 
            datediff(lit(current_date), col("last_purchase_date"))) \
        .withColumn("frequency", col("transaction_count")) \
        .withColumn("monetary", col("total_lifetime_value")) \
        .withColumn("avg_days_between_purchases",
            round(datediff(col("last_purchase_date"), col("first_purchase_date")) / 
                  (col("transaction_count") - 1), 1))
    
    # Join with customer demographics
    enriched_metrics = rfm_metrics.join(customers_df, "customer_id", "left")
    
    # Customer segmentation based on RFM
    segmented_customers = enriched_metrics \
        .withColumn("recency_score",
            when(col("recency_days") <= 30, 5)
            .when(col("recency_days") <= 90, 4)
            .when(col("recency_days") <= 180, 3)
            .when(col("recency_days") <= 365, 2)
            .otherwise(1)) \
        .withColumn("frequency_score",
            when(col("frequency") >= 20, 5)
            .when(col("frequency") >= 10, 4)
            .when(col("frequency") >= 5, 3)
            .when(col("frequency") >= 2, 2)
            .otherwise(1)) \
        .withColumn("monetary_score",
            when(col("monetary") >= 5000, 5)
            .when(col("monetary") >= 2000, 4)
            .when(col("monetary") >= 1000, 3)
            .when(col("monetary") >= 500, 2)
            .otherwise(1)) \
        .withColumn("rfm_score", 
            col("recency_score") + col("frequency_score") + col("monetary_score")) \
        .withColumn("customer_segment",
            when(col("rfm_score") >= 13, "Champions")
            .when(col("rfm_score") >= 11, "Loyal Customers")
            .when(col("rfm_score") >= 9, "Potential Loyalists")
            .when(col("rfm_score") >= 7, "New Customers")
            .when(col("rfm_score") >= 5, "Promising")
            .otherwise("At Risk"))
    
    return segmented_customers

def calculate_product_metrics(sales_df, products_df):
    """Calculate product performance metrics"""
    print("Calculating product metrics...")
    
    # Product sales metrics
    product_metrics = sales_df.groupBy("category", "product_name").agg(
        count("*").alias("times_sold"),
        sum("quantity").alias("total_quantity_sold"),
        sum("total_amount").alias("total_revenue"),
        avg("total_amount").alias("avg_sale_value"),
        countDistinct("customer_id").alias("unique_customers"),
        countDistinct("region").alias("regions_sold")
    )
    
    # Join with product cost data
    enriched_products = product_metrics.join(
        products_df, ["category", "product_name"], "left")
    
    # Calculate profitability metrics
    profit_metrics = enriched_products \
        .withColumn("total_cost", col("total_quantity_sold") * col("cost_price")) \
        .withColumn("total_profit", col("total_revenue") - col("total_cost")) \
        .withColumn("profit_margin_actual", 
            round(col("total_profit") / col("total_revenue") * 100, 2)) \
        .withColumn("roi_percent", 
            round(col("total_profit") / col("total_cost") * 100, 2))
    
    return profit_metrics

# TODO: Calculate comprehensive metrics
customer_analytics = calculate_customer_metrics(clean_sales, enriched_customers)
product_analytics = calculate_product_metrics(clean_sales, products_df)

# Display insights
print("\n=== Customer Segmentation Summary ===")
customer_analytics.groupBy("customer_segment").agg(
    count("*").alias("customer_count"),
    avg("total_lifetime_value").alias("avg_lifetime_value"),
    avg("transaction_count").alias("avg_frequency")
).orderBy(desc("avg_lifetime_value")).show()

print("\n=== Top Performing Products ===")
product_analytics.orderBy(desc("total_profit")).select(
    "category", "product_name", "total_revenue", "total_profit", "roi_percent"
).show(10)
```

#### Task 5.4: Data Pipeline Automation
```python
def create_summary_tables(sales_df, customers_df, products_df):
    """Create summary tables for reporting"""
    
    # Daily summary
    daily_summary = sales_df.groupBy("date_formatted", "region").agg(
        sum("total_amount").alias("daily_revenue"),
        count("*").alias("daily_transactions"),
        countDistinct("customer_id").alias("unique_customers"),
        avg("total_amount").alias("avg_order_value")
    ).withColumn("created_timestamp", current_timestamp())
    
    # Monthly category performance
    monthly_category = sales_df.groupBy("year", "month", "category").agg(
        sum("total_amount").alias("monthly_revenue"),
        sum("quantity").alias("monthly_quantity"),
        countDistinct("customer_id").alias("unique_customers"),
        count("*").alias("transaction_count")
    ).withColumn("created_timestamp", current_timestamp())
    
    # Customer loyalty trends
    loyalty_trends = sales_df.join(customers_df, "customer_id") \
        .groupBy("year", "month", "loyalty_tier").agg(
            sum("total_amount").alias("tier_revenue"),
            countDistinct("customer_id").alias("active_customers"),
            avg("total_amount").alias("avg_spend_per_transaction")
        ).withColumn("created_timestamp", current_timestamp())
    
    return daily_summary, monthly_category, loyalty_trends

def save_pipeline_results(daily_summary, monthly_category, loyalty_trends, 
                         customer_analytics, product_analytics):
    """Save all pipeline results"""
    
    # Save as Parquet for analytics
    print("Saving results as Parquet...")
    daily_summary.write.mode("overwrite").parquet("/home/jovyan/data/parquet/daily_summary")
    monthly_category.write.mode("overwrite").parquet("/home/jovyan/data/parquet/monthly_category")
    loyalty_trends.write.mode("overwrite").parquet("/home/jovyan/data/parquet/loyalty_trends")
    customer_analytics.write.mode("overwrite").parquet("/home/jovyan/data/parquet/customer_analytics")
    product_analytics.write.mode("overwrite").parquet("/home/jovyan/data/parquet/product_analytics")
    
    # Save key insights as CSV for business users
    print("Saving business reports as CSV...")
    
    # Top customers report
    top_customers = customer_analytics.select(
        "customer_id", "first_name", "last_name", "total_lifetime_value", 
        "transaction_count", "customer_segment", "loyalty_tier"
    ).orderBy(desc("total_lifetime_value")).limit(100)
    
    top_customers.coalesce(1).write.mode("overwrite") \
        .option("header", "true") \
        .csv("/home/jovyan/data/csv/top_customers_report")
    
    # Product performance report
    product_report = product_analytics.select(
        "category", "product_name", "total_revenue", "total_profit", 
        "times_sold", "unique_customers", "roi_percent"
    ).orderBy(desc("total_profit"))
    
    product_report.coalesce(1).write.mode("overwrite") \
        .option("header", "true") \
        .csv("/home/jovyan/data/csv/product_performance_report")

# TODO: Run the complete pipeline
daily_summary, monthly_category, loyalty_trends = create_summary_tables(
    clean_sales, enriched_customers, products_df)

save_pipeline_results(daily_summary, monthly_category, loyalty_trends,
                     customer_analytics, product_analytics)

print("✅ Data pipeline completed successfully!")
print("\nGenerated outputs:")
print("- Daily summary (Parquet)")
print("- Monthly category performance (Parquet)")  
print("- Customer loyalty trends (Parquet)")
print("- Customer analytics (Parquet)")
print("- Product analytics (Parquet)")
print("- Top customers report (CSV)")
print("- Product performance report (CSV)")
```

#### Task 5.5: Performance Monitoring and Optimization
```python
def monitor_pipeline_performance():
    """Monitor and report pipeline performance metrics"""
    
    # Check cache usage
    print("=== Cache Usage ===")
    cached_tables = spark.sql("CACHE TABLE sales").collect()
    
    # Monitor partition sizes
    print("\n=== Partition Analysis ===")
    sales_partitions = clean_sales.rdd.glom().map(len).collect()
    print(f"Partition sizes: {sales_partitions}")
    print(f"Min partition size: {min(sales_partitions)}")
    print(f"Max partition size: {max(sales_partitions)}")
    print(f"Partition skew ratio: {max(sales_partitions) / min(sales_partitions):.2f}")
    
    # Check for shuffle operations in last query
    print("\n=== Last Query Analysis ===")
    last_query = customer_analytics.join(product_analytics.select("category").distinct(), "category")
    last_query.explain()
    
    # Memory usage recommendations
    print("\n=== Optimization Recommendations ===")
    if max(sales_partitions) / min(sales_partitions) > 2:
        print("⚠️  High partition skew detected - consider repartitioning")
    
    total_cores = spark.sparkContext.defaultParallelism
    total_partitions = len(sales_partitions)
    if total_partitions < total_cores:
        print(f"⚠️  Under-partitioned: {total_partitions} partitions for {total_cores} cores")
    elif total_partitions > total_cores * 3:
        print(f"⚠️  Over-partitioned: {total_partitions} partitions for {total_cores} cores")
    else:
        print("✅ Partitioning looks optimal")

monitor_pipeline_performance()
```

**Expected Output**: A complete, production-ready data pipeline with monitoring and optimization.

---

## Final Challenge: Streaming Simulation (Advanced)
**Estimated time: 60-90 minutes**

### Learning Goals:
- Understand streaming concepts
- Implement near real-time processing
- Handle late-arriving data

### Challenge Task:
```python
def simulate_streaming_pipeline():
    """Simulate a streaming data pipeline"""
    
    # Read JSON events as a streaming source (simulated)
    events_df = spark.read.json("/home/jovyan/data/json/web_events.json")
    
    # Process events in micro-batches (simulating streaming)
    processed_events = events_df \
        .withColumn("timestamp", to_timestamp("timestamp")) \
        .withColumn("hour", hour("timestamp")) \
        .withColumn("session_length_minutes", 
                   round(col("session_duration") / 60, 2)) \
        .withColumn("is_conversion", 
                   col("event_type") == "purchase")
    
    # Real-time analytics (simulated)
    # Hourly event counts
    hourly_stats = processed_events.groupBy("hour", "event_type").count()
    
    # User session analysis
    user_sessions = processed_events.groupBy("user_id").agg(
        count("*").alias("total_events"),
        max("session_duration").alias("max_session_duration"),
        countDistinct("device").alias("devices_used"),
        sum(col("is_conversion").cast("int")).alias("conversions")
    )
    
    # Alert conditions (simulated)
    high_activity_users = user_sessions.filter(col("total_events") > 50)
    
    print("=== Streaming Analytics Results ===")
    print(f"High activity users: {high_activity_users.count()}")
    
    print("\nHourly activity pattern:")
    hourly_stats.orderBy("hour", "event_type").show()
    
    print("\nTop active users:")
    user_sessions.orderBy(desc("total_events")).show(10)
    
    return processed_events, user_sessions

# TODO: Implement the streaming simulation
streaming_results = simulate_streaming_pipeline()
```

---

## Exercise Submission Guidelines

### For Each Exercise:
1. **Code**: Submit your completed Python/SQL code
2. **Output**: Include screenshots or text output of your results
3. **Analysis**: Write 2-3 sentences explaining key insights
4. **Performance**: Note any performance observations or optimizations you discovered

### Evaluation Criteria:
- **Correctness**: Does the code execute without errors?
- **Completeness**: Are all TODO items completed?
- **Insights**: Can you extract meaningful business insights?
- **Optimization**: Do you understand performance implications?
- **Code Quality**: Is the code readable and well-structured?

### Advanced Challenges (Bonus):
1. **Custom UDF**: Create a User Defined Function for specific business logic
2. **Window Functions**: Implement complex analytical functions using window operations
3. **Graph Analysis**: Use GraphX to analyze customer-product relationships
4. **ML Pipeline**: Build an end-to-end machine learning pipeline with MLlib
5. **Integration**: Connect to external databases (PostgreSQL) for data loading/saving

---

## Additional Resources

### Documentation:
- [Spark SQL Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)
- [DataFrame API](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql.html)
- [Performance Tuning](https://spark.apache.org/docs/latest/tuning.html)

### Practice Datasets:
- Use the provided sample data for consistency
- Try with your own datasets for additional practice
- Kaggle datasets for more complex scenarios

### Community:
- Stack Overflow for specific questions
- Spark user mailing lists
- Local Spark meetup groups

### Next Steps:
1. Deploy on cloud platforms (AWS EMR, Databricks)
2. Learn Scala for better performance
3. Explore Delta Lake for data lakes
4. Study advanced optimization techniques
5. Build real production pipelines

---

**Good luck with your Spark journey! 🚀**

Remember: The key to mastering Spark is practice with real data and real problems. Start small, understand the fundamentals, then build more complex solutions.