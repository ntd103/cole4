# Hadoop/HDFS and Python Integration Demo

A comprehensive demonstration of Hadoop Distributed File System (HDFS) integration with Python using Docker Compose. This demo provides hands-on experience with HDFS operations, data processing, and distributed computing concepts.

## 📋 Table of Contents

- [Overview](#overview)
- [Demo Structure](#demo-structure)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Progressive Exercises](#progressive-exercises)
- [Minimum Deliverables](#minimum-deliverables)
- [Advanced Features](#advanced-features)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)

## 🎯 Overview

This demo teaches students how to:
- Set up a Hadoop cluster using Docker Compose
- Interact with HDFS using Python
- Perform distributed data processing
- Implement data pipelines
- Handle large-scale data operations

### Learning Objectives

- Understand HDFS architecture and concepts
- Master Python-HDFS integration
- Develop data processing pipelines
- Implement error handling and logging
- Create scalable data solutions

## 🏗️ Demo Structure

```
D9 - Hadoop Introduction/
├── README.md                          # This comprehensive guide
├── docker-compose.yml                 # Hadoop cluster configuration
├── setup.sh                          # Setup script
├── cleanup.sh                        # Cleanup script
├── run_exercise.sh                    # Exercise runner
├── config/                           # Hadoop configuration files
│   ├── hadoop.env                    # Environment variables
│   ├── core-site.xml                # Core configuration
│   └── hdfs-site.xml                # HDFS configuration
├── python-client/                   # Python client container
│   ├── Dockerfile                   # Python environment setup
│   ├── requirements.txt             # Python dependencies
│   ├── hdfs_demo.py                 # Main demonstration script
│   └── hadoop-conf/                 # Hadoop configuration for Python
│       └── core-site.xml
├── data/                            # Sample data files
│   ├── sample_employees.csv         # Employee dataset
│   └── sample_text.txt              # Text processing sample
└── exercises/                       # Progressive learning exercises
    ├── exercise1_basic_operations.py      # HDFS basics
    ├── exercise2_data_processing.py       # Data analysis
    ├── exercise3_text_processing.py       # Text analytics
    └── exercise4_advanced_pipeline.py     # Complete pipeline
```

### Component Architecture

#### Hadoop Cluster Components
- **Namenode**: Manages filesystem metadata and namespace
- **Datanode 1 & 2**: Store actual data blocks with replication
- **Python Client**: Interactive environment for HDFS operations

#### Key Services
- **HDFS Web UI**: http://localhost:9870 (Namenode)
- **Datanode UI**: http://localhost:9864 (Primary Datanode)
- **HDFS API**: Port 8020 for programmatic access

## 🔧 Prerequisites

### Required Software
- Docker (>= 20.10)
- Docker Compose (>= 2.0)
- 4GB+ available RAM
- 10GB+ available disk space

### Optional Tools
- Python 3.9+ (for local development)
- Web browser (for UI access)
- Text editor/IDE

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Clone or navigate to the demo directory
cd "D9 - Hadoop Introduction"

# Make scripts executable
chmod +x setup.sh cleanup.sh run_exercise.sh

# Start the Hadoop cluster
./setup.sh
```

### 2. Verify Installation
```bash
# Check cluster status
docker-compose ps

# Access HDFS Web UI
open http://localhost:9870

# Enter Python client
docker exec -it hadoop-python-client bash
```

### 3. Run Demo
```bash
# Run the complete demonstration
./run_exercise.sh demo

# Or run individual exercises
./run_exercise.sh 1  # Basic operations
./run_exercise.sh 2  # Data processing
./run_exercise.sh 3  # Text analysis
./run_exercise.sh 4  # Advanced pipeline
```

### 4. Cleanup
```bash
# Stop the cluster
./cleanup.sh

# Remove all data (optional)
docker-compose down -v
```

## 🎓 Progressive Exercises

### Exercise 1: Basic HDFS Operations (Beginner)
**File**: `exercises/exercise1_basic_operations.py`

**Objectives**:
- Connect to HDFS using Python
- Create directory structures
- Upload and download files
- List directory contents
- Get file metadata

**Key Concepts**:
- HDFS client initialization
- File system navigation
- Basic I/O operations
- Error handling

**Expected Deliverables**:
- Working HDFS connection
- Created directory: `/exercises/exercise1/`
- Uploaded file: `employees.csv`
- Downloaded file verification
- File information display

### Exercise 2: Data Processing (Intermediate)
**File**: `exercises/exercise2_data_processing.py`

**Objectives**:
- Read CSV data from HDFS
- Perform statistical analysis
- Filter and group data
- Save processed results

**Key Concepts**:
- Pandas integration with HDFS
- Data validation and cleaning
- Statistical computations
- Multi-format output

**Expected Deliverables**:
- Statistical summary report
- Filtered datasets (high earners, young employees)
- City-wise salary analysis
- Age group distribution
- Results saved in multiple formats

### Exercise 3: Text Processing and Word Count (Intermediate-Advanced)
**File**: `exercises/exercise3_text_processing.py`

**Objectives**:
- Process large text files
- Implement word count algorithms
- Analyze text patterns
- Generate comprehensive reports

**Key Concepts**:
- Text preprocessing and cleaning
- Regular expressions
- Frequency analysis
- Stop word filtering

**Expected Deliverables**:
- Word frequency analysis
- Text statistics (sentences, paragraphs)
- Most common words identification
- Comprehensive text analysis report
- Multiple output formats (JSON, CSV, TXT)

### Exercise 4: Advanced Data Pipeline (Advanced)
**File**: `exercises/exercise4_advanced_pipeline.py`

**Objectives**:
- Build complete data processing pipelines
- Implement robust error handling
- Create reusable data processing classes
- Generate business insights

**Key Concepts**:
- Object-oriented pipeline design
- Data validation and quality checks
- Logging and monitoring
- Scalable data processing patterns

**Expected Deliverables**:
- Complete data pipeline class
- Data validation system
- Automated cleaning and processing
- Business insights generation
- Comprehensive reporting system

## 📊 Minimum Deliverables

### For Students

#### Exercise 1 Deliverables
- [ ] Successful HDFS connection
- [ ] Directory creation: `/exercises/exercise1/`
- [ ] File upload: `sample_employees.csv`
- [ ] File listing with details
- [ ] File download verification
- [ ] Screenshot of HDFS Web UI

#### Exercise 2 Deliverables
- [ ] Data loading from HDFS
- [ ] Statistical analysis results
- [ ] Filtered datasets (2 files)
- [ ] Aggregated analysis reports
- [ ] Performance metrics

#### Exercise 3 Deliverables
- [ ] Text preprocessing implementation
- [ ] Word count algorithm
- [ ] Top 10 frequent words
- [ ] Text statistics report
- [ ] Pattern analysis results

#### Exercise 4 Deliverables
- [ ] Complete pipeline class
- [ ] Data validation system
- [ ] Error handling implementation
- [ ] Business insights report
- [ ] Pipeline execution logs

### For Instructors

#### Assessment Criteria
- **Code Quality** (25%): Clean, documented, error-free code
- **Functionality** (30%): All requirements implemented correctly
- **Analysis** (25%): Meaningful insights and interpretations
- **Documentation** (20%): Clear explanations and comments

#### Grading Rubric
- **A (90-100%)**: All deliverables + advanced features
- **B (80-89%)**: Core deliverables with minor issues
- **C (70-79%)**: Basic functionality with some missing features
- **D (60-69%)**: Partial implementation
- **F (<60%)**: Major functionality missing

## 🔬 Advanced Features

### Performance Monitoring
- Container resource usage
- HDFS storage utilization
- Processing time metrics
- Memory consumption analysis

### Scalability Testing
- Large file processing
- Multiple concurrent operations
- Replication factor testing
- Fault tolerance scenarios

### Real-world Integration
- External data source connectivity
- API integration examples
- Batch processing workflows
- Streaming data simulation

## 🛠️ Troubleshooting

### Common Issues

#### Container Startup Problems
```bash
# Check Docker daemon
docker --version
docker-compose --version

# Check available resources
docker system df
docker system prune  # Clean up if needed
```

#### HDFS Connection Issues
```bash
# Check Namenode status
docker exec hadoop-namenode hdfs dfsadmin -report

# Check network connectivity
docker exec hadoop-python-client ping namenode

# Restart services
docker-compose restart
```

#### Python Package Issues
```bash
# Enter container and check packages
docker exec -it hadoop-python-client bash
pip list | grep hdfs

# Reinstall if needed
pip install --force-reinstall hdfs3
```

#### Memory/Performance Issues
```bash
# Check container resources
docker stats

# Increase Docker memory allocation
# (Docker Desktop: Settings > Resources > Memory)
```

### Debug Commands
```bash
# View logs
docker-compose logs namenode
docker-compose logs datanode1
docker-compose logs python-client

# Check HDFS filesystem
docker exec hadoop-namenode hdfs fsck /

# Monitor resources
docker exec hadoop-namenode hdfs dfsadmin -report
```

## 📚 Resources

### Official Documentation
- [Apache Hadoop Documentation](https://hadoop.apache.org/docs/)
- [HDFS Architecture Guide](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html)
- [Python hdfs3 Library](https://hdfs3.readthedocs.io/)

### Additional Learning
- [Hadoop Ecosystem Overview](https://hadoop.apache.org/docs/stable/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

### Sample Datasets
- Employee data (included)
- Text analysis samples (included)
- Large dataset generators (in exercises)

## 🤝 Contributing

### For Instructors
- Add new exercises in the `exercises/` directory
- Update configuration in `config/` as needed
- Enhance the demo script with new features
- Add more sample datasets

### For Students
- Report issues or bugs
- Suggest improvements
- Share interesting analysis results
- Create additional visualization examples

## 📝 License

This educational demo is provided for academic use. Please ensure proper attribution when using or modifying the content.

---

**Happy Learning! 🎉**

This demo provides a comprehensive introduction to Hadoop/HDFS with Python integration. Work through the exercises progressively, and don't hesitate to explore beyond the basic requirements. The skills learned here form the foundation for big data processing and distributed computing.

For questions or support, refer to the troubleshooting section or consult the provided resources.
