# Hadoop Ecosystem Demo with Docker Compose

## Overview
This comprehensive demo showcases the Hadoop ecosystem including HDFS, YARN, Hive, HBase, Sqoop, and Python integration. The entire setup runs in Docker containers for easy deployment and learning.

## Architecture Components
- **Hadoop HDFS**: Distributed file system
- **YARN**: Resource manager and job scheduler
- **Hive**: Data warehouse software for querying large datasets
- **HBase**: NoSQL column-family database
- **Sqoop**: Tool for transferring data between Hadoop and relational databases
- **MySQL**: Sample relational database for Sqoop demonstrations
- **Python**: For data processing and integration scripts
- **Jupyter Notebook**: Interactive development environment

## Demo Structure
```
D10 - Hadoop Ecosystem/
├── docker-compose.yml          # Main orchestration file
├── data/                       # Sample datasets
│   ├── employees.csv
│   ├── sales.csv
│   └── customers.json
├── hive/                       # Hive configurations and scripts
│   ├── scripts/
│   └── warehouse/
├── hbase/                      # HBase configurations
│   └── scripts/
├── sqoop/                      # Sqoop jobs and configurations
│   └── jobs/
├── python/                     # Python integration scripts
│   ├── notebooks/
│   ├── scripts/
│   └── requirements.txt
├── mysql/                      # MySQL initialization
│   └── init/
└── exercises/                  # Progressive student exercises
    ├── exercise-1/
    ├── exercise-2/
    ├── exercise-3/
    └── exercise-4/
```

## Quick Start

### Prerequisites
- Docker (v20.10+)
- Docker Compose (v2.0+)
- At least 8GB RAM allocated to Docker

### ✅ Quick Verification
Run the automated test script to verify everything is working:
```bash
./test-hive.sh
```

This will test:
- Service status and health
- Hive database/table access
- Data querying and aggregation
- Join operations across tables

**Expected output**: All tests should pass showing employee data, sales data, and aggregated results.

### Manual Startup
1. Clone this repository
2. Navigate to the project directory
3. Start the environment:
   ```bash
   docker-compose up -d
   ```
4. Wait for all services to be healthy (check with `docker-compose ps`)
5. Access the web interfaces:
   - Hadoop NameNode: http://localhost:9870
   - YARN ResourceManager: http://localhost:8088
   - HBase Master: http://localhost:16010
   - Jupyter Notebook: http://localhost:8888 (token: hadoop)

### Stopping the Environment
```bash
docker-compose down
```

## Service Endpoints
| Service | Port | Web UI |
|---------|------|--------|
| HDFS NameNode | 9000 | http://localhost:9870 |
| YARN ResourceManager | 8032 | http://localhost:8088 |
| Hive Server2 | 10000 | - |
| HBase Master | 16000 | http://localhost:16010 |
| HBase RegionServer | 16020 | http://localhost:16030 |
| MySQL | 3306 | - |
| Jupyter Notebook | 8888 | http://localhost:8888 |

## Progressive Exercises

### Exercise 1: HDFS Basics (Beginner)
**Objective**: Learn HDFS commands and file operations
**Deliverables**:
- Upload sample data to HDFS
- Create directory structure
- Perform basic file operations
- Screenshot of HDFS web UI showing uploaded files

### Exercise 2: Hive Data Warehousing (Intermediate)
**Objective**: Create tables, load data, and perform queries
**Deliverables**:
- Create external and managed tables
- Load CSV data into Hive tables
- Write and execute 5 different SQL queries
- Export query results

### Exercise 3: HBase NoSQL Operations (Intermediate)
**Objective**: Work with column-family database
**Deliverables**:
- Create HBase tables with column families
- Insert, update, and query data
- Implement row key design strategy
- Performance comparison report

### Exercise 4: Data Integration with Sqoop (Advanced)
**Objective**: Transfer data between RDBMS and Hadoop
**Deliverables**:
- Import data from MySQL to HDFS
- Export processed data from Hive to MySQL
- Create incremental import job
- Data lineage documentation

### Exercise 5: Python Integration (Advanced)
**Objective**: Process big data using Python
**Deliverables**:
- Python script to process HDFS data
- Jupyter notebook with data analysis
- Integration with Hive using Python
- Visualization of results

## Minimum Deliverables

### For Instructors
1. **Working Docker Environment**: All services running and accessible
2. **Sample Datasets**: Representative data for all exercises
3. **Step-by-step Guides**: Detailed instructions for each exercise
4. **Verification Scripts**: Automated checks for exercise completion
5. **Assessment Rubrics**: Clear grading criteria

### For Students
1. **Exercise Completion Reports**: Document for each exercise with:
   - Commands executed
   - Screenshots of results
   - Explanations of concepts learned
   - Challenges faced and solutions
2. **Final Integration Project**: Combining all technologies in a mini data pipeline
3. **Performance Analysis**: Comparison of different approaches and tools
4. **Presentation**: 10-minute demo of completed work

## Troubleshooting

### Common Issues
1. **Out of Memory**: Increase Docker memory allocation
2. **Port Conflicts**: Check if ports are already in use
3. **Slow Startup**: Wait longer for services to initialize
4. **Connection Refused**: Verify all containers are running

### Useful Commands
```bash
# Check container status
docker-compose ps

# View logs for specific service
docker-compose logs [service-name]

# Restart specific service
docker-compose restart [service-name]

# Access container shell
docker-compose exec [service-name] bash
```

## Learning Resources
- [Apache Hadoop Documentation](https://hadoop.apache.org/docs/)
- [Apache Hive Documentation](https://hive.apache.org/)
- [Apache HBase Documentation](https://hbase.apache.org/)
- [Apache Sqoop Documentation](https://sqoop.apache.org/)

## Assessment Criteria

### Technical Skills (70%)
- HDFS operations and understanding (15%)
- Hive query writing and optimization (20%)
- HBase data modeling and operations (15%)
- Sqoop data transfer jobs (10%)
- Python integration and scripting (10%)

### Documentation and Presentation (30%)
- Clear documentation of processes (15%)
- Problem-solving approach (10%)
- Presentation quality (5%)

## Support
For questions and issues:
1. Check the troubleshooting section
2. Review container logs
3. Consult official documentation
4. Ask instructor for assistance

---
*Last updated: September 2025*
