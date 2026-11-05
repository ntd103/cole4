# Comprehensive Spark Demo for Students

## 1. Business Requirements

### Business Context: E-Commerce Analytics Platform

**Company**: GlobalMart - An international e-commerce platform
**Challenge**: Process and analyze large-scale transaction data to gain insights

**Business Objectives**:
1. Track sales performance across regions and product categories
2. Identify customer purchasing patterns and behavior
3. Detect fraudulent transactions
4. Optimize inventory based on demand patterns
5. Generate real-time dashboards for business stakeholders

**Data Sources**:
- Transaction logs (sales, returns, refunds)
- Customer profile data
- Product catalog
- Website clickstream data

**Key Metrics Required**:
- Revenue by region, category, and time period
- Customer lifetime value (CLV)
- Average order value (AOV)
- Product performance metrics
- Fraud detection score

**Scale**:
- 10M+ transactions per month
- 5M+ active customers
- 100K+ products
- Real-time processing required for fraud detection

---

## 2. Solution Architecture

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Data Sources Layer                       │
├─────────────────────────────────────────────────────────────┤
│  CSV Files  │  JSON Logs  │  Parquet Files  │  PostgreSQL  │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   Ingestion Layer                            │
├─────────────────────────────────────────────────────────────┤
│              Spark Batch / Structured Streaming              │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  Processing Layer                            │
├─────────────────────────────────────────────────────────────┤
│  • Data Cleaning      • Transformations                      │
│  • Feature Engineering • Aggregations                        │
│  • ML Models          • Window Functions                     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    Storage Layer                             │
├─────────────────────────────────────────────────────────────┤
│  • MinIO (S3-compatible)  • PostgreSQL (metadata)            │
│  • Parquet files          • Delta Lake (optional)            │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  Analytics Layer                             │
├─────────────────────────────────────────────────────────────┤
│  Jupyter Notebooks  │  Spark SQL  │  Visualization          │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

- **Spark**: 3.5.0 (latest stable)
- **Python**: 3.11
- **Jupyter**: For interactive analysis
- **PostgreSQL**: Metadata storage
- **MinIO**: S3-compatible object storage
- **Docker Compose**: Container orchestration

### Component Responsibilities

1. **Spark Master/Workers**: Distributed computation
2. **Jupyter**: Interactive development and EDA
3. **PostgreSQL**: Store processed results and metadata
4. **MinIO**: Store raw and processed data files

---

## 3. Data Model

### Star Schema Design

#### Fact Table: `fact_transactions`
```
transaction_id (PK)      : BIGINT
customer_id (FK)         : BIGINT
product_id (FK)          : BIGINT
date_id (FK)             : INT
region_id (FK)           : INT
transaction_timestamp    : TIMESTAMP
quantity                 : INT
unit_price              : DECIMAL(10,2)
total_amount            : DECIMAL(10,2)
discount_amount         : DECIMAL(10,2)
tax_amount              : DECIMAL(10,2)
payment_method          : STRING
transaction_status      : STRING (completed, refunded, failed)
fraud_score             : FLOAT
```

#### Dimension Table: `dim_customers`
```
customer_id (PK)        : BIGINT
first_name              : STRING
last_name               : STRING
email                   : STRING
registration_date       : DATE
customer_segment        : STRING (premium, regular, new)
country                 : STRING
city                    : STRING
age_group               : STRING
```

#### Dimension Table: `dim_products`
```
product_id (PK)         : BIGINT
product_name            : STRING
category                : STRING
sub_category            : STRING
brand                   : STRING
supplier_id             : INT
unit_cost               : DECIMAL(10,2)
stock_quantity          : INT
```

#### Dimension Table: `dim_date`
```
date_id (PK)            : INT
date                    : DATE
year                    : INT
quarter                 : INT
month                   : INT
week                    : INT
day_of_week             : INT
is_weekend              : BOOLEAN
is_holiday              : BOOLEAN
```

#### Dimension Table: `dim_regions`
```
region_id (PK)          : INT
region_name             : STRING
country                 : STRING
continent               : STRING
timezone                : STRING
```

### Data Relationships
- Fact table connects to all dimension tables via foreign keys
- Enables efficient OLAP queries and aggregations
- Supports drill-down and roll-up operations

---

## 4. Project Structure

``` 
spark-demo/
│
├── docker-compose.yml
├── Dockerfile.spark
├── Dockerfile.jupyter
│
├── notebooks/
│   ├── 01_data_generation.ipynb
│   ├── 02_data_ingestion.ipynb
│   ├── 03_eda_analysis.ipynb
│   ├── 04_transformations.ipynb
│   ├── 05_aggregations.ipynb
│   └── 06_ml_fraud_detection.ipynb
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── output/
│
├── scripts/
│   ├── init_postgres.sql
│   └── generate_sample_data.py
│
└── requirements.txt
```

---

## 5. Learning Objectives

By the end of this demo, students will understand:

1. **Spark Architecture**: Master/Worker model, executors, tasks
2. **DataFrames & Datasets**: Core Spark abstractions
3. **Transformations vs Actions**: Lazy evaluation concept
4. **Partitioning**: How to optimize data distribution
5. **Joins**: Broadcast joins, shuffle joins, optimization
6. **Aggregations**: GroupBy, window functions, pivot
7. **Performance Tuning**: Caching, persistence, repartitioning
8. **Data Formats**: Parquet, CSV, JSON - when to use each
9. **Structured Streaming**: Real-time data processing
10. **ML with Spark**: MLlib basics for classification

---

## Next Steps

We'll now create:
1. Docker Compose configuration
2. Sample data generation scripts
3. Jupyter notebooks for hands-on learning
4. SQL initialization scripts