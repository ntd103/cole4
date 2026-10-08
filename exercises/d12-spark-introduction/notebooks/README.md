# Apache Spark Demo Notebooks

This directory contains comprehensive Jupyter notebooks demonstrating Apache Spark capabilities using PySpark. These notebooks are designed to work with the Docker Compose setup provided in this project.

## 📚 Notebook Overview

### 1. [Spark Basics](01_spark_basics.ipynb)
**Beginner Level** - Introduction to Apache Spark fundamentals
- SparkSession and SparkContext setup
- RDDs (Resilient Distributed Datasets) operations
- DataFrames and basic transformations
- Reading and writing data in various formats
- Spark SQL basics and temporary views
- Performance monitoring and caching

**Learning Outcomes:**
- Understand Spark's distributed computing model
- Master basic data operations and transformations
- Learn to work with structured data using DataFrames
- Explore Spark's lazy evaluation concepts

### 2. [Advanced Analytics](02_advanced_analytics.ipynb)
**Intermediate Level** - Complex data processing and analytics
- Complex joins and multi-table operations
- Window functions and advanced aggregations
- Time series analysis and temporal patterns
- Customer segmentation with RFM analysis
- Data quality assessment and validation
- Advanced SQL operations and optimization

**Learning Outcomes:**
- Perform sophisticated data analysis workflows
- Implement customer analytics and segmentation
- Master window functions and complex aggregations
- Apply data quality best practices

### 3. [Streaming Processing](03_streaming_processing.ipynb)
**Intermediate Level** - Real-time data processing with Structured Streaming
- Streaming DataFrames and real-time processing
- Windowed aggregations and watermarking
- Stream-to-static joins and enrichment
- Multiple output sinks (console, files, memory)
- State management and checkpointing
- Complex event processing patterns

**Learning Outcomes:**
- Build real-time analytics applications
- Handle late-arriving data with watermarking
- Implement streaming ETL pipelines
- Monitor and manage streaming applications

### 4. [Machine Learning](04_machine_learning.ipynb)
**Advanced Level** - ML at scale with Spark MLlib
- Feature engineering and data preparation
- Classification models (customer value prediction)
- Regression models (lifetime value forecasting)
- Clustering for customer segmentation
- Recommendation systems with ALS
- Hyperparameter tuning and cross-validation
- Model persistence and deployment patterns

**Learning Outcomes:**
- Build end-to-end ML pipelines
- Implement various ML algorithms at scale
- Perform model evaluation and optimization
- Deploy and monitor ML models in production

### 5. [Database Integration](05_database_integration.ipynb)
**Advanced Level** - Enterprise data integration patterns
- JDBC connectivity with PostgreSQL
- ETL/ELT workflows and data pipelines
- Partitioned reads and performance optimization
- Incremental data loading (CDC patterns)
- Data quality validation and monitoring
- Production best practices and security

**Learning Outcomes:**
- Integrate Spark with enterprise databases
- Build robust ETL/ELT pipelines
- Implement data quality frameworks
- Apply production-ready integration patterns

## 🚀 Getting Started

### Prerequisites
1. **Docker and Docker Compose** installed on your system
2. **At least 8GB RAM** available for containers
3. **10GB free disk space** for data and containers

### Setup Instructions

1. **Start the Environment**
   ```bash
   # From the project root directory
   docker-compose up -d
   
   # Wait for all services to start (about 2-3 minutes)
   ```

2. **Generate Sample Data**
   ```bash
   # Generate the demo datasets
   python3 scripts/generate_sample_data.py
   ```

3. **Access Jupyter Lab**
   - Open your browser to `http://localhost:8889`
   - Password: `jupyter` (if prompted)
   - Navigate to the `work` directory to find the notebooks

4. **Verify Spark Cluster**
   - Spark Master UI: `http://localhost:8080`
   - You should see 2 worker nodes connected

### Environment Details

The demo environment provides:
- **Spark Master**: Cluster coordination and job scheduling
- **2 Spark Workers**: Distributed processing (2 cores, 2GB RAM each)
- **Jupyter Lab**: Interactive notebook environment with PySpark
- **PostgreSQL**: Database for integration examples
- **Sample Datasets**: Sales, customers, and products data

## 📊 Sample Datasets

The notebooks use realistic sample datasets:

- **Sales Data** (10,000 transactions)
  - Transaction details, amounts, dates
  - Product categories and regional information
  - Customer purchase history

- **Customer Data** (1,000 customers)  
  - Demographics (age, city, loyalty tier)
  - Registration dates and customer IDs
  - Segmentation attributes

- **Product Catalog** (15 products)
  - Product details and categories
  - Cost and pricing information
  - Profit margin calculations

- **Web Events** (5,000 events)
  - User interaction data for streaming demos
  - Session information and device types
  - Purchase and engagement events

## 🎯 Learning Path

### For Beginners
1. Start with **Spark Basics** to understand core concepts
2. Practice with the sample datasets
3. Experiment with different transformations and actions

### For Data Analysts
1. Begin with **Spark Basics** for foundation
2. Focus on **Advanced Analytics** for complex queries
3. Explore **Database Integration** for real-world workflows

### For Data Scientists
1. Complete **Spark Basics** and **Advanced Analytics**
2. Deep dive into **Machine Learning** for ML pipelines
3. Use **Streaming Processing** for real-time ML applications

### For Data Engineers
1. Master all notebooks in sequence
2. Focus on **Streaming Processing** and **Database Integration**
3. Implement production patterns from best practices sections

## 🔧 Troubleshooting

### Common Issues

**Spark Connection Problems**
```python
# Check if Spark master is accessible
spark = SparkSession.builder \
    .appName("Test") \
    .master("spark://spark-master:7077") \
    .getOrCreate()
```

**Memory Issues**
- Reduce data sizes in examples
- Adjust Spark configurations:
```python
.config("spark.executor.memory", "1g") \
.config("spark.driver.memory", "1g")
```

**Database Connection Issues**
- Verify PostgreSQL container is running: `docker ps`
- Check connection parameters in notebook
- Ensure database initialization completed

### Performance Tips

1. **Optimize Partitioning**
   ```python
   # Repartition data for better performance
   df.repartition(4, "customer_id")
   ```

2. **Cache Frequently Used DataFrames**
   ```python
   df.cache()
   df.count()  # Trigger caching
   ```

3. **Use Appropriate File Formats**
   ```python
   # Parquet for analytical workloads
   df.write.parquet("path/to/data")
   ```

## 📚 Additional Resources

### Documentation
- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)
- [PySpark API Reference](https://spark.apache.org/docs/latest/api/python/)
- [Spark SQL Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)

### Learning Materials
- [Spark: The Definitive Guide](https://learning.oreilly.com/library/view/spark-the-definitive/9781491912201/)
- [Learning Spark, 2nd Edition](https://learning.oreilly.com/library/view/learning-spark-2nd/9781492050032/)
- [Apache Spark Online Courses](https://www.coursera.org/courses?query=apache%20spark)

### Community
- [Apache Spark User Mailing List](https://spark.apache.org/community.html)
- [Stack Overflow - Apache Spark](https://stackoverflow.com/questions/tagged/apache-spark)
- [Spark Summit Recordings](https://databricks.com/sparkaisummit)

## 🤝 Contributing

Feel free to:
- Report issues or bugs
- Suggest improvements to notebooks
- Add new examples or use cases
- Share your own Spark experiences

## 📄 License

These notebooks are provided as educational material under the MIT License. Feel free to use and modify for your learning and projects.

---

**Happy Learning!** 🎉

*Remember: The best way to learn Spark is by doing. Experiment with the code, modify examples, and apply concepts to your own datasets.*
