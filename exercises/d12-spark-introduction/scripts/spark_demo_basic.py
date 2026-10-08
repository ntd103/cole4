from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import os

def create_spark_session():
    """Create Spark session with appropriate configurations"""
    return SparkSession.builder \
        .appName("Spark Basic Demo") \
        .master("spark://spark-master:7077") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .getOrCreate()

def demo_rdd_operations(spark):
    """Demonstrate RDD operations"""
    print("=== RDD Operations Demo ===")
    sc = spark.sparkContext
    
    # Create RDD from collection
    numbers = sc.parallelize(range(1, 101))
    
    # Transformations (lazy)
    even_numbers = numbers.filter(lambda x: x % 2 == 0)
    squared_evens = even_numbers.map(lambda x: x ** 2)
    
    # Actions (trigger execution)
    print(f"Count of even numbers: {even_numbers.count()}")
    print(f"First 5 squared even numbers: {squared_evens.take(5)}")
    print(f"Sum of squared even numbers: {squared_evens.sum()}")
    
    # Demonstrate partitions
    print(f"Number of partitions: {numbers.getNumPartitions()}")
    
    # Cache for reuse
    squared_evens.cache()
    print(f"Cached RDD - Max value: {squared_evens.max()}")

def demo_dataframe_operations(spark):
    """Demonstrate DataFrame operations"""
    print("\n=== DataFrame Operations Demo ===")
    
    # Read sales data
    sales_df = spark.read.csv("/home/spark/data/csv/sales_data.csv", header=True, inferSchema=True)
    
    print(f"Sales data shape: {sales_df.count()} rows, {len(sales_df.columns)} columns")
    
    # Show schema
    print("\nSales Data Schema:")
    sales_df.printSchema()
    
    # Show first few rows
    print("\nFirst 5 rows:")
    sales_df.show(5)
    
    # Basic aggregations
    print("\nBasic Statistics:")
    sales_df.select("quantity", "unit_price", "total_amount").describe().show()
    
    # Group by operations
    print("\nSales by Category:")
    category_sales = sales_df.groupBy("category") \
        .agg(
            sum("total_amount").alias("total_sales"),
            count("*").alias("transaction_count"),
            avg("total_amount").alias("avg_order_value")
        ) \
        .orderBy(desc("total_sales"))
    
    category_sales.show()
    
    # Filtering and transformation
    print("\nHigh-value transactions (>$1000):")
    high_value = sales_df.filter(col("total_amount") > 1000) \
        .select("transaction_id", "category", "product_name", "total_amount", "date") \
        .orderBy(desc("total_amount"))
    
    high_value.show(10)

def demo_sql_operations(spark):
    """Demonstrate Spark SQL operations"""
    print("\n=== Spark SQL Operations Demo ===")
    
    # Read data and create temporary view
    sales_df = spark.read.csv("/home/spark/data/csv/sales_data.csv", header=True, inferSchema=True)
    customers_df = spark.read.csv("/home/spark/data/csv/customers.csv", header=True, inferSchema=True)
    
    sales_df.createOrReplaceTempView("sales")
    customers_df.createOrReplaceTempView("customers")
    
    # Complex SQL query
    query = """
    SELECT 
        c.loyalty_tier,
        COUNT(*) as customer_count,
        SUM(s.total_amount) as total_sales,
        AVG(s.total_amount) as avg_order_value,
        MAX(s.total_amount) as max_order_value
    FROM sales s
    JOIN customers c ON s.customer_id = c.customer_id
    GROUP BY c.loyalty_tier
    ORDER BY total_sales DESC
    """
    
    result = spark.sql(query)
    print("\nSales by Loyalty Tier:")
    result.show()
    
    # Window functions
    window_query = """
    SELECT 
        category,
        date,
        total_amount,
        ROW_NUMBER() OVER (PARTITION BY category ORDER BY total_amount DESC) as rank,
        SUM(total_amount) OVER (PARTITION BY category) as category_total
    FROM sales
    QUALIFY rank <= 3
    """
    
    top_sales = spark.sql(window_query)
    print("\nTop 3 sales per category:")
    top_sales.show()

def demo_advanced_operations(spark):
    """Demonstrate advanced Spark operations"""
    print("\n=== Advanced Operations Demo ===")
    
    # Read multiple datasets
    sales_df = spark.read.csv("/home/spark/data/csv/sales_data.csv", header=True, inferSchema=True)
    customers_df = spark.read.csv("/home/spark/data/csv/customers.csv", header=True, inferSchema=True)
    products_df = spark.read.csv("/home/spark/data/csv/products.csv", header=True, inferSchema=True)
    
    # Complex join operation
    enriched_sales = sales_df \
        .join(customers_df, "customer_id", "left") \
        .join(products_df.select("category", "product_name", "cost_price", "profit_margin"), 
              ["category", "product_name"], "left") \
        .withColumn("profit", col("total_amount") * col("profit_margin")) \
        .withColumn("age_group", 
                   when(col("age") < 30, "Young")
                   .when(col("age") < 50, "Middle")
                   .otherwise("Senior"))
    
    # Customer segmentation analysis
    print("\nCustomer Segmentation Analysis:")
    segmentation = enriched_sales.groupBy("age_group", "loyalty_tier") \
        .agg(
            count("*").alias("transaction_count"),
            sum("total_amount").alias("total_revenue"),
            sum("profit").alias("total_profit"),
            countDistinct("customer_id").alias("unique_customers")
        ) \
        .withColumn("avg_revenue_per_customer", 
                   round(col("total_revenue") / col("unique_customers"), 2)) \
        .orderBy("age_group", "loyalty_tier")
    
    segmentation.show()
    
    # Pivot operation
    print("\nRevenue by Region and Category (Pivot):")
    pivot_data = sales_df.groupBy("region") \
        .pivot("category") \
        .agg(sum("total_amount")) \
        .fillna(0)
    
    pivot_data.show()

def demo_streaming_simulation(spark):
    """Demonstrate streaming-like operations"""
    print("\n=== Streaming Simulation Demo ===")
    
    # Read JSON data
    events_df = spark.read.json("/home/spark/data/json/web_events.json")
    
    print("Web Events Schema:")
    events_df.printSchema()
    
    # Streaming-style aggregations
    print("\nEvent Analysis:")
    event_stats = events_df.groupBy("event_type", "device") \
        .agg(
            count("*").alias("event_count"),
            avg("session_duration").alias("avg_session_duration")
        ) \
        .orderBy("event_type", "device")
    
    event_stats.show()
    
    # Time-based analysis
    events_with_hour = events_df \
        .withColumn("timestamp", to_timestamp("timestamp")) \
        .withColumn("hour", hour("timestamp"))
    
    hourly_activity = events_with_hour.groupBy("hour") \
        .agg(count("*").alias("events")) \
        .orderBy("hour")
    
    print("\nHourly Activity Pattern:")
    hourly_activity.show(24)

def demo_performance_optimization(spark):
    """Demonstrate performance optimization techniques"""
    print("\n=== Performance Optimization Demo ===")
    
    sales_df = spark.read.csv("/home/spark/data/csv/sales_data.csv", header=True, inferSchema=True)
    
    # Cache frequently used DataFrame
    sales_df.cache()
    
    # Optimize partitioning
    print(f"Original partitions: {sales_df.rdd.getNumPartitions()}")
    
    # Repartition for better performance
    optimized_df = sales_df.repartition(4, "region")
    print(f"Optimized partitions: {optimized_df.rdd.getNumPartitions()}")
    
    # Broadcast join simulation (small dataset)
    customers_df = spark.read.csv("/home/spark/data/csv/customers.csv", header=True, inferSchema=True)
    
    # Force broadcast hint
    from pyspark.sql.functions import broadcast
    joined_df = sales_df.join(broadcast(customers_df), "customer_id")
    
    print("\nBroadcast join completed")
    print(f"Joined data count: {joined_df.count()}")
    
    # Show execution plan (explain)
    print("\nExecution Plan:")
    joined_df.explain()

def save_results_demo(spark):
    """Demonstrate saving results in different formats"""
    print("\n=== Save Results Demo ===")
    
    sales_df = spark.read.csv("/home/spark/data/csv/sales_data.csv", header=True, inferSchema=True)
    
    # Create summary data
    monthly_summary = sales_df \
        .withColumn("year_month", date_format("date", "yyyy-MM")) \
        .groupBy("year_month", "category") \
        .agg(
            sum("total_amount").alias("total_sales"),
            count("*").alias("transaction_count"),
            avg("total_amount").alias("avg_order_value")
        )
    
    # Save as Parquet (columnar format)
    monthly_summary.write \
        .mode("overwrite") \
        .parquet("/home/spark/data/parquet/monthly_summary")
    
    print("✅ Saved monthly summary as Parquet")
    
    # Save as JSON
    monthly_summary.write \
        .mode("overwrite") \
        .json("/home/spark/data/json/monthly_summary")
    
    print("✅ Saved monthly summary as JSON")
    
    # Save as CSV with single file
    monthly_summary.coalesce(1).write \
        .mode("overwrite") \
        .option("header", "true") \
        .csv("/home/spark/data/csv/monthly_summary")
    
    print("✅ Saved monthly summary as CSV")

def main():
    """Main demo function"""
    print("🚀 Starting Spark Demo...")
    
    # Create Spark session
    spark = create_spark_session()
    
    try:
        # Run all demos
        demo_rdd_operations(spark)
        demo_dataframe_operations(spark)
        demo_sql_operations(spark)
        demo_advanced_operations(spark)
        demo_streaming_simulation(spark)
        demo_performance_optimization(spark)
        save_results_demo(spark)
        
        print("\n✅ All demos completed successfully!")
        
        # Show Spark UI information
        print(f"\n📊 Spark UI available at: http://localhost:8080")
        print(f"📊 Application UI: {spark.sparkContext.uiWebUrl}")
        
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
    finally:
        spark.stop()

if __name__ == "__main__":
    main()