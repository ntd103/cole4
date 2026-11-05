# Exercise 1: HDFS Basics (Beginner Level)

## Objective
Learn fundamental HDFS operations including file management, directory operations, and basic commands.

## Prerequisites
- Docker environment running
- NameNode accessible at http://localhost:9870

## Tasks

### Task 1.1: HDFS Directory Operations (20 points)
Create the following directory structure in HDFS:
```
/user/student/
├── input/
├── output/
└── backup/
```

**Commands to execute:**
```bash
# Access the namenode container
docker exec -it namenode bash

# Create directories
hdfs dfs -mkdir -p /user/student/input
hdfs dfs -mkdir -p /user/student/output
hdfs dfs -mkdir -p /user/student/backup

# List the created directories
hdfs dfs -ls /user/student/
```

**Deliverable:** Screenshot of the directory listing output

### Task 1.2: File Upload and Management (25 points)
Upload the sample data files to HDFS and perform basic file operations.

**Commands to execute:**
```bash
# Upload files to HDFS
hdfs dfs -put /data/employees.csv /user/student/input/
hdfs dfs -put /data/sales.csv /user/student/input/
hdfs dfs -put /data/customers.json /user/student/input/

# Verify uploads
hdfs dfs -ls /user/student/input/

# Check file details
hdfs dfs -stat "%n %o %r %u %g %s %b %y" /user/student/input/employees.csv

# View first 10 lines of a file
hdfs dfs -head /user/student/input/employees.csv
```

**Deliverable:** 
- Screenshot of file listing
- Text file with the output of the stat command for all three files

### Task 1.3: File Operations (25 points)
Perform copy, move, and delete operations on HDFS files.

**Commands to execute:**
```bash
# Copy a file within HDFS
hdfs dfs -cp /user/student/input/employees.csv /user/student/backup/

# Move a file
hdfs dfs -mv /user/student/backup/employees.csv /user/student/backup/employees_backup.csv

# Create a new file with some content
echo "HDFS Test File" | hdfs dfs -put - /user/student/output/test.txt

# View the file content
hdfs dfs -cat /user/student/output/test.txt

# Get file from HDFS to local filesystem
hdfs dfs -get /user/student/backup/employees_backup.csv /tmp/

# List all files recursively
hdfs dfs -ls -R /user/student/
```

**Deliverable:** 
- Screenshot of recursive directory listing
- Verification that the file was successfully downloaded to /tmp/

### Task 1.4: HDFS Web Interface Exploration (20 points)
Explore the HDFS web interface and document your findings.

**Steps:**
1. Open http://localhost:9870 in your browser
2. Navigate to "Utilities" → "Browse the file system"
3. Browse to your created directories
4. View file details and blocks
5. Check the "Datanodes" tab to see cluster information

**Deliverable:** 
- Screenshot of the web interface showing your directory structure
- Screenshot of datanode information
- Brief report (200 words) on what you observed

### Task 1.5: HDFS Storage Analysis (10 points)
Analyze HDFS storage usage and replication.

**Commands to execute:**
```bash
# Check HDFS storage usage
hdfs dfs -du -h /user/student/

# Check disk usage summary
hdfs dfs -df -h

# View file system check
hdfs fsck /user/student/ -files -blocks -locations
```

**Deliverable:** 
- Text file with all command outputs
- Brief explanation of replication factor and block size

## Submission Requirements

Create a folder named `exercise1_[your_name]` containing:

1. **screenshots/** folder with all required screenshots
2. **commands.txt** - All commands you executed
3. **outputs.txt** - All command outputs
4. **report.md** - Your analysis and observations (minimum 300 words)
5. **reflection.md** - What you learned and challenges faced (minimum 200 words)

## Grading Rubric

| Component | Points | Criteria |
|-----------|---------|----------|
| Task 1.1 | 20 | Correct directory structure created |
| Task 1.2 | 25 | Files uploaded and verified correctly |
| Task 1.3 | 25 | File operations performed correctly |
| Task 1.4 | 20 | Web interface exploration documented |
| Task 1.5 | 10 | Storage analysis completed |
| **Total** | **100** | |

## Common Issues and Solutions

1. **Permission Denied**: Make sure you're running commands as the hadoop user
2. **Container Not Running**: Check with `docker ps` and restart if needed
3. **Out of Space**: Check available disk space with `hdfs dfs -df`
4. **Network Issues**: Verify all containers are on the same network

## Additional Resources
- [HDFS Commands Guide](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/HDFSCommands.html)
- [HDFS Architecture](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html)
