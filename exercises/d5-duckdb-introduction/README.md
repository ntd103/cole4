# DuckDB vs Pandas Performance Demo

A comprehensive demonstration of DuckDB's advantages over Pandas for single-machine data processing, featuring real-world datasets and performance benchmarks.

## 🎯 What's Included

### Presentation (15-20 slides)
- **Why DuckDB over Pandas**: Memory efficiency, performance, and scalability
- **Technical deep-dive**: Architecture, vectorized execution, query optimization
- **Hands-on demo**: Real performance comparisons with large datasets
- **Best practices**: When to use DuckDB vs other tools

### Demo Environment
- **Docker-based setup**: Reproducible environment with Jupyter Lab
- **Large sample datasets**: 10M+ transactions, 1M customers, 100K products
- **Performance benchmarks**: Direct Pandas vs DuckDB comparisons
- **Advanced features**: Window functions, joins, time series analysis

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- 8GB+ RAM recommended
- 5GB+ free disk space

### Setup Instructions

1. **Clone and enter the demo directory**
   ```bash
   # Create project directory
   mkdir duckdb-demo
   cd duckdb-demo
   ```

2. **Create the required files**
   Copy all the provided files into your directory:
   - `docker-compose.yml`
   - `Dockerfile`
   - `Dockerfile.datagen`
   - `generate_sample_data.py`
   - `jupyter_lab_config.py`
   - `Makefile`

3. **Create directory structure**
   ```bash
   mkdir -p notebooks data scripts
   ```

4. **Start the demo environment**
   ```bash
   make up
   ```
   
   This will:
   - Build Docker images
   - Start Jupyter Lab server
   - Generate sample datasets (10M+ records)
   - Set up the demo environment

5. **Access Jupyter Lab**
   - URL: http://localhost:8888
   - Token: `duckdb-demo`

## 📊 Dataset Overview

The demo includes four realistic datasets:

| Dataset | Records | Description |
|---------|---------|-------------|
| **Transactions** | 10,000,000 | Customer purchases with products, amounts, dates |
| **Customers** | 1,000,000 | Customer demographics and segments |
| **Products** | 100,000 | Product catalog with categories and pricing |
| **Daily Metrics** | 731 | Time series data for trend analysis |

### File Sizes
- Parquet format: ~2.5GB total
- CSV format: ~4.8GB total
- Perfect for demonstrating out-of-core processing

## 🔬 Performance Tests

### Benchmark Scenarios

1. **Basic Aggregation**
   - Revenue by product category
   - Customer spending summaries
   - Transaction count analysis

2. **Complex Joins**
   - Customer + Transaction analysis
   - Multi-table aggregations
   - Segment performance metrics

3. **Window Functions**
   - Customer ranking by spending
   - Running totals and percentiles
   - Time-based analytics

4. **Time Series Analysis**
   - Monthly trends and growth rates
   - Moving averages
   - Seasonal pattern detection

### Expected Performance Gains
- **Aggregations**: 10-15x faster than Pandas
- **Joins**: 8-12x faster than Pandas
- **Window Functions**: 12-18x faster than Pandas
- **Memory Usage**: 3-5x more efficient

## 📁 Project Structure

```
duckdb-demo/
├── docker-compose.yml          # Docker services definition
├── Dockerfile                  # Jupyter environment
├── Dockerfile.datagen         # Data generation container
├── Makefile                   # Easy commands
├── README.md                  # This file
├── generate_sample_data.py    # Data generation script
├── jupyter_lab_config.py      # Jupyter configuration
├── notebooks/                 # Demo notebooks (auto-created)
│   └── duckdb_vs_pandas_demo.ipynb
├── data/                      # Generated datasets
│   ├── transactions.parquet
│   ├── customers.parquet
│   ├── products.parquet
│   ├── daily_metrics.parquet
│   └── dataset_summary.json
└── scripts/                   # Utility scripts
    └── performance_monitor.py
```

## 🛠️ Available Commands

```bash
# Environment management
make up        # Start all services
make down      # Stop services
make build     # Rebuild images
make clean     # Clean everything
make reset     # Full reset

# Development
make logs      # View logs
make shell     # Access container
make notebook  # Open Jupyter (auto-detects OS)
make status    # Check service status

# Data management
make data      # Regenerate datasets
```

## 📚 Demo Notebooks

### 1. Performance Comparison (`duckdb_vs_pandas_demo.ipynb`)
- Direct performance benchmarks
- Memory usage monitoring
- Visualization of results
- Export capabilities

### 2. Advanced Features Demo
- Complex SQL queries
- JSON and array operations
- Window functions
- Time series analysis

### 3. Integration Examples
- Pandas interoperability
- Export to various formats
- Real-world use cases

## 🎯 Presentation Flow

### Slides 1-4: Problem & Solution
- Current limitations with Pandas
- Why DuckDB is the answer
- Performance overview

### Slides 5-8: Technical Deep-dive
- Vectorized execution
- Memory management
- Query optimization
- Architecture components

### Slides 9-12: Integration & Use Cases
- Python integration patterns
- Ecosystem compatibility
- When to use DuckDB

### Slides 13-16: Practical Implementation
- Installation and setup
- Performance optimization
- Best practices

### Slides 17-20: Demo & Conclusion
- Live demonstration
- Key takeaways
- Next steps

## 🔧 Customization

### Adjusting Dataset Sizes
Edit `generate_sample_data.py`:

```python
# Reduce for faster generation/lower memory
customers_df = generate_customers(100_000)        # 1M -> 100K
transactions_df = generate_transactions(1_000_000) # 10M -> 1M
```

### Memory Configuration
Edit `docker-compose.yml`:

```yaml
environment:
  - DUCKDB_MEMORY_LIMIT=4GB  # Adjust based on available RAM
```

### Adding Custom Datasets
Place files in `./data/` directory:
- Parquet files: Direct DuckDB access
- CSV files: Streaming support
- JSON files: Native JSON querying

## 🚨 Troubleshooting

### Common Issues

1. **Out of Memory Errors**
   ```bash
   # Reduce dataset size or increase Docker memory
   docker system prune -f
   make clean && make up
   ```

2. **Port Already in Use**
   ```bash
   # Change port in docker-compose.yml
   ports:
     - "8889:8888"  # Use different port
   ```

3. **Slow Data Generation**
   ```bash
   # Check available resources
   docker stats
   
   # Reduce dataset sizes in generate_sample_data.py
   ```

4. **Container Build Failures**
   ```bash
   # Clear Docker cache and rebuild
   make reset
   ```

### Performance Tips

1. **Allocate Sufficient RAM**: 8GB+ recommended
2. **Use SSD Storage**: Faster I/O for large datasets
3. **Close Other Applications**: Maximize available resources
4. **Monitor Resource Usage**: Use `htop` or Activity Monitor

## 📈 Expected Demo Results

### Performance Improvements
- **10-15x** faster aggregations
- **8-12x** faster joins
- **12-18x** faster window functions
- **3-5x** lower memory usage

### Audience Impact
- Clear demonstration of DuckDB advantages
- Hands-on experience with real datasets
- Understanding of when to choose DuckDB
- Practical implementation knowledge

## 🔗 Additional Resources

### Documentation
- [DuckDB Official Docs](https://duckdb.org/docs/)
- [Python API Reference](https://duckdb.org/docs/api/python/overview)
- [SQL Reference](https://duckdb.org/docs/sql/introduction)

### Learning Materials
- [DuckDB Blog](https://duckdb.org/news/)
- [Performance Benchmarks](https://duckdb.org/2021/05/14/sql-on-pandas.html)
- [Integration Examples](https://github.com/duckdb/duckdb/tree/master/examples)

### Community
- [GitHub Repository](https://github.com/duckdb/duckdb)
- [Discord Community](https://discord.duckdb.org/)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/duckdb)

## 🤝 Contributing

Found an issue or want to improve the demo?

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with `make reset`
5. Submit a pull request

## 📜 License

This demo is provided under MIT License. See LICENSE file for details.

## 🙏 Acknowledgments

- DuckDB team for the amazing database engine
- Jupyter Project for the notebook environment
- Faker library for realistic data generation
- Docker for containerization capabilities

---

**Ready to see DuckDB in action? Run `make up` and start exploring!** 🦆