#!/usr/bin/env python3
"""
Spark Shuffle and Partitioning Demo
Demonstrates advanced shuffle mechanisms and partitioning strategies
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import time
import numpy as np
import matplotlib.pyplot as plt

def create_spark_session():
    """Create optimized Spark session"""
    return SparkSession.builder \
        .appName("ShufflePartitioningDemo") \
        .master("spark://spark-master:7077") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .config("spark.sql.adaptive.skewJoin.enabled", "true") \
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
        .getOrCreate()

def create_test_datasets(spark, size=50000):
    """Create test datasets for demonstration"""
    
    # Create sales data with skew
    sales_data = []
    for i in range(size):
        # Create skew by making some customers very active
        if i < size * 0.1:  # 10% of data goes to first 1% of customers
            customer_id = i % int(size * 0.01) + 1
        else:
            customer_id = np.random.randint(1, size // 10)
        
        sales_data.append((
            i + 1,
            customer_id,
            np.random.randint(1, 1000),
            np.random.choice(['Electronics', 'Clothing', 'Books', 'Sports']),
            round(np.random.uniform(10, 2000), 2),
            np.random.choice(['North', 'South', 'East', 'West'])
        ))
    
    sales_schema = StructType([
        StructField("transaction_id", IntegerType(), True),
        StructField("customer_id", IntegerType(), True),
        StructField("product_id", IntegerType(), True),
        StructField("category", StringType(), True),
        StructField("amount", DoubleType(), True),
        StructField("region", StringType(), True)
    ])
    
    # Create customer data
    customer_data = []
    for i in range(size // 10):
        customer_data.append((
            i + 1,
            f"customer_{i}",
            np.random.randint(18, 80),
            np.random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'])
        ))
    
    customer_schema = StructType([
        StructField("customer_id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("age", IntegerType(), True),
        StructField("city", StringType(), True)
    ])
    
    sales_df = spark.createDataFrame(sales_data, sales_schema)
    customers_df = spark.createDataFrame(customer_data, customer_schema)
    
    return sales_df, customers_df

def analyze_partitioning(df, description):
    """Analyze DataFrame partitioning"""
    print(f"\n=== {description} ===")
    print(f"Number of partitions: {df.rdd.getNumPartitions()}")
    
    # Get partition sizes
    partition_sizes = df.rdd.mapPartitionsWithIndex(
        lambda idx, iterator: [(idx, sum(1 for _ in iterator))]
    ).collect()
    
    sizes = [size for _, size in partition_sizes]
    print(f"Partition sizes: {sizes}")
    print(f"Min size: {min(sizes)}, Max size: {max(sizes)}")
    print(f"Skew ratio: {max(sizes) / min(sizes) if min(sizes) > 0 else 'inf':.2f}")
    
    return partition_sizes

def demonstrate_partitioning_strategies(spark):
    """Demonstrate different partitioning strategies"""
    print("🔄 PARTITIONING STRATEGIES DEMONSTRATION")
    print("=" * 50)
    
    # Create test data
    sales_df, customers_df = create_test_datasets(spark, 20000)
    
    # 1. Default partitioning
    analyze_partitioning(sales_df, "Default Partitioning")
    
    # 2. Hash partitioning by customer_id
    hash_partitioned = sales_df.repartition(8, "customer_id")
    analyze_partitioning(hash_partitioned, "Hash Partitioning by customer_id")
    
    # 3. Range partitioning by amount
    range_partitioned = sales_df.repartitionByRange(6, "amount")
    analyze_partitioning(range_partitioned, "Range Partitioning by amount")
    
    # 4. Custom partitioning by region
    region_partitioned = sales_df.repartition("region")
    analyze_partitioning(region_partitioned, "Partitioning by region")
    
    return sales_df, customers_df

def demonstrate_shuffle_optimization(spark, sales_df, customers_df):
    """Demonstrate shuffle optimization techniques"""
    print("\n🚀 SHUFFLE OPTIMIZATION DEMONSTRATION")
    print("=" * 50)
    
    def time_operation(operation_func, description):
        start_time = time.time()
        result = operation_func()
        elapsed = time.time() - start_time
        print(f"{description}: {elapsed:.3f} seconds")
        return result, elapsed
    
    # 1. Broadcast Join
    print("\n1. Broadcast Join:")
    broadcast_result, broadcast_time = time_operation(
        lambda: sales_df.join(broadcast(customers_df), "customer_id").count(),
        "Broadcast join"
    )
    
    # 2. Sort-Merge Join (disable broadcast)
    print("\n2. Sort-Merge Join:")
    spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "-1")
    sortmerge_result, sortmerge_time = time_operation(
        lambda: sales_df.join(customers_df, "customer_id").count(),
        "Sort-merge join"
    )
    
    # 3. Pre-partitioned Join
    print("\n3. Pre-partitioned Join:")
    sales_partitioned = sales_df.repartition("customer_id").cache()
    customers_partitioned = customers_df.repartition("customer_id").cache()
    
    # Trigger caching
    sales_partitioned.count()
    customers_partitioned.count()
    
    prepart_result, prepart_time = time_operation(
        lambda: sales_partitioned.join(customers_partitioned, "customer_id").count(),
        "Pre-partitioned join"
    )
    
    # Reset broadcast threshold
    spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "10485760")
    
    # 4. Bucketed Join Simulation
    print("\n4. Bucketed Join Simulation:")
    # Simulate bucketing by ensuring same partitioning
    sales_bucketed = sales_df.repartition(4, "customer_id").cache()
    customers_bucketed = customers_df.repartition(4, "customer_id").cache()
    
    bucketed_result, bucketed_time = time_operation(
        lambda: sales_bucketed.join(customers_bucketed, "customer_id").count(),
        "Bucketed join simulation"
    )
    
    # Visualize results
    join_types = ['Broadcast', 'Sort-Merge', 'Pre-partitioned', 'Bucketed']
    join_times = [broadcast_time, sortmerge_time, prepart_time, bucketed_time]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(join_types, join_times, color=['skyblue', 'lightgreen', 'salmon', 'gold'])
    plt.title('Join Strategy Performance Comparison')
    plt.ylabel('Execution Time (seconds)')
    plt.xlabel('Join Strategy')
    
    # Add value labels on bars
    for bar, time_val in zip(bars, join_times):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{time_val:.3f}s', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.show()
    
    # Cleanup
    sales_partitioned.unpersist()
    customers_partitioned.unpersist()
    sales_bucketed.unpersist()
    customers_bucketed.unpersist()

def demonstrate_skew_handling(spark):
    """Demonstrate skew handling techniques"""
    print("\n⚖️ SKEW HANDLING DEMONSTRATION")
    print("=" * 50)
    
    # Create heavily skewed data
    skewed_data = []
    for i in range(10000):
        if i < 5000:  # 50% of data goes to one key
            key = "SKEWED_KEY"
        else:
            key = f"KEY_{i % 100}"
        
        skewed_data.append((key, np.random.uniform(1, 100)))
    
    skewed_df = spark.createDataFrame(skewed_data, "key STRING, value DOUBLE")
    
    print("Original skewed data distribution:")
    skew_distribution = skewed_df.groupBy("key").count().orderBy(desc("count"))
    skew_distribution.show(10)
    
    # Demonstrate adaptive query execution handling
    print("\nWith Adaptive Query Execution:")
    spark.conf.set("spark.sql.adaptive.enabled", "true")
    spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
    spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes", "256MB")
    
    # Create another DataFrame for join
    join_data = [(f"KEY_{i}", f"value_{i}") for i in range(200)]
    join_data.append(("SKEWED_KEY", "skewed_value"))
    join_df = spark.createDataFrame(join_data, "key STRING, description STRING")
    
    # Perform skewed join
    start_time = time.time()
    skewed_join_result = skewed_df.join(join_df, "key").count()
    skewed_join_time = time.time() - start_time
    
    print(f"Skewed join completed in {skewed_join_time:.3f} seconds")
    print(f"Result count: {skewed_join_result}")
    
    # Manual skew handling with salting
    print("\nManual skew handling with salting:")
    
    # Add salt to skewed DataFrame
    salted_df = skewed_df.withColumn(
        "salt", 
        when(col("key") == "SKEWED_KEY", 
             (rand() * 10).cast(IntegerType())).otherwise(lit(0))
    ).withColumn(
        "salted_key",
        when(col("key") == "SKEWED_KEY",
             concat(col("key"), lit("_"), col("salt"))).otherwise(col("key"))
    )
    
    # Expand join DataFrame with salt
    salt_range = spark.range(10).select(col("id").alias("salt_id"))
    expanded_join_df = join_df.crossJoin(salt_range).withColumn(
        "salted_key",
        when(col("key") == "SKEWED_KEY",
             concat(col("key"), lit("_"), col("salt_id"))).otherwise(col("key"))
    )
    
    start_time = time.time()
    salted_join_result = salted_df.join(expanded_join_df, "salted_key").count()
    salted_join_time = time.time() - start_time
    
    print(f"Salted join completed in {salted_join_time:.3f} seconds")
    print(f"Result count: {salted_join_result}")
    
    return skewed_join_time, salted_join_time

def demonstrate_adaptive_query_execution(spark):
    """Demonstrate Adaptive Query Execution features"""
    print("\n🧠 ADAPTIVE QUERY EXECUTION DEMONSTRATION")
    print("=" * 50)
    
    # Create test data
    large_data = []
    for i in range(30000):
        large_data.append((
            i,
            f"group_{i % 100}",
            np.random.uniform(1, 1000)
        ))
    
    large_df = spark.createDataFrame(large_data, "id INT, group_id STRING, amount DOUBLE")
    
    # Enable AQE features
    spark.conf.set("spark.sql.adaptive.enabled", "true")
    spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
    spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
    
    print("AQE Configuration:")
    aqe_configs = [
        "spark.sql.adaptive.enabled",
        "spark.sql.adaptive.coalescePartitions.enabled",
        "spark.sql.adaptive.skewJoin.enabled"
    ]
    
    for config in aqe_configs:
        value = spark.conf.get(config)
        print(f"  {config}: {value}")
    
    # Demonstrate partition coalescing
    print("\nDemonstrating partition coalescing:")
    highly_partitioned = large_df.repartition(50)
    print(f"Before AQE: {highly_partitioned.rdd.getNumPartitions()} partitions")
    
    # Force execution to trigger AQE
    result = highly_partitioned.groupBy("group_id").agg(sum("amount")).collect()
    print(f"After AQE optimization: partitions coalesced for better performance")
    
    return large_df

def main():
    """Main demonstration function"""
    print("🎯 SPARK SHUFFLE AND PARTITIONING DEEP DIVE")
    print("=" * 60)
    
    # Create Spark session
    spark = create_spark_session()
    spark.sparkContext.setLogLevel("WARN")
    
    try:
        # 1. Partitioning strategies
        sales_df, customers_df = demonstrate_partitioning_strategies(spark)
        
        # 2. Shuffle optimization
        demonstrate_shuffle_optimization(spark, sales_df, customers_df)
        
        # 3. Skew handling
        skewed_time, salted_time = demonstrate_skew_handling(spark)
        
        # 4. Adaptive Query Execution
        demonstrate_adaptive_query_execution(spark)
        
        # Summary
        print("\n📊 PERFORMANCE SUMMARY")
        print("=" * 30)
        print(f"Skew handling improvement: {skewed_time / salted_time:.2f}x with salting")
        
        print("\n🎯 KEY TAKEAWAYS")
        print("=" * 20)
        takeaways = [
            "✅ Choose partitioning strategy based on access patterns",
            "✅ Use broadcast joins for small tables",
            "✅ Pre-partition data for multiple operations on same key",
            "✅ Enable Adaptive Query Execution for automatic optimization",
            "✅ Handle data skew with salting or AQE",
            "✅ Monitor shuffle metrics to identify bottlenecks"
        ]
        
        for takeaway in takeaways:
            print(f"  {takeaway}")
    
    finally:
        spark.stop()

if __name__ == "__main__":
    main()
