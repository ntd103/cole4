# Unix/Linux Demo Environment - Comprehensive Guide

## Overview

This Docker Compose setup creates a complete Unix/Linux learning environment with multiple interconnected containers that demonstrate all aspects of Unix/Linux system administration, networking, and shell scripting covered in the presentation.

## Environment Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Main Demo     │    │   Web Server    │    │   Database      │
│   Container     │────│   (nginx)       │    │   (MySQL)       │
│ (ubuntu:22.04)  │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FTP Server    │    │   Log Generator │    │   Demo Network  │
│   (pure-ftpd)   │────│   Container     │────│   (Bridge)      │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- At least 2GB free RAM
- 5GB free disk space
- Ports 8080, 21, 30000-30009 available on host

### 1. Start the Environment

```bash
# Navigate to the demo directory
cd "/Users/lap16470/Cole/Demo/D8 - Unix:Linux"

# Start all containers
docker-compose up -d

# Verify all containers are running
docker-compose ps
```

### 2. Access the Main Demo Container

```bash
# Enter the main demo container
docker exec -it unix-linux-demo bash

# Navigate to the demo directory
cd /demo

# Run the master demo script
bash scripts/master-demo.sh
```

### 3. Verify Environment

```bash
# Check container status
docker-compose ps

# Expected output:
# unix-linux-demo    Up
# demo-webserver     Up
# demo-database      Up
# demo-ftpserver     Up
# demo-logger        Up
```

## Detailed Component Guide

### Main Demo Container (unix-linux-demo)

**Purpose**: Primary learning environment with all Unix/Linux tools
**Image**: ubuntu:22.04
**Features**:
- Full Ubuntu environment with essential tools
- Pre-configured users (root, demouser)
- SSH server for remote access demonstrations
- All demo scripts and sample data

**Access Methods**:
```bash
# Interactive shell
docker exec -it unix-linux-demo bash

# As demo user
docker exec -it -u demouser unix-linux-demo bash

# SSH (from within container network)
ssh demouser@unix-linux-demo  # Password: demo123
```

### Web Server (demo-webserver)

**Purpose**: Target for network utility demonstrations
**Image**: nginx:alpine
**Access**: http://localhost:8080

**Demonstrations**:
- wget/curl downloads
- HTTP response analysis
- Network connectivity testing
- Service discovery

**Usage Examples**:
```bash
# From main container
curl http://web-server/
wget http://web-server/demo-data.json
ping -c 3 web-server
```

### Database Server (demo-database)

**Purpose**: Background service for process management demos
**Image**: mysql:8.0
**Credentials**:
- Root: rootpass
- User: demouser / demo123
- Database: demoapp

**Usage Examples**:
```bash
# Test database connectivity
nc -z db-server 3306
telnet db-server 3306

# Monitor database processes
ps aux | grep mysql
```

### FTP Server (demo-ftpserver)

**Purpose**: File transfer protocol demonstrations
**Image**: stilliard/pure-ftpd
**Access**: ftp://localhost:21
**Credentials**: demouser / demo123

**Usage Examples**:
```bash
# FTP from main container
ftp ftp-server
# Login: demouser / demo123

# SFTP alternative
sftp demouser@ftp-server
```

### Log Generator (demo-logger)

**Purpose**: Continuous log generation for pipes/filters demos
**Location**: Logs written to `/demo/logs/`

**Generated Files**:
- `app.log`: Application logs with INFO/ERROR/WARNING
- `access.log`: User access logs

**Usage Examples**:
```bash
# Monitor logs in real-time
tail -f /demo/logs/app.log

# Analyze log patterns
grep "ERROR" /demo/logs/app.log | wc -l
awk '/ERROR/ {print $1, $2}' /demo/logs/app.log
```

## Demo Script Guide

### Available Demonstrations

| Script | Section | Description |
|--------|---------|-------------|
| `01-getting-started.sh` | Getting Started | Basic commands, help system |
| `02-file-management.sh` | File Management | Creating, viewing, copying files |
| `03-directory-management.sh` | Directory Management | Directory operations, navigation |
| `04-file-permissions.sh` | File Permissions | Permission management, umask |
| `05-environment.sh` | Environment | Variables, aliases, configuration |
| `06-pipes-filters.sh` | Pipes and Filters | grep, awk, sed, sort, uniq |
| `07-process-management.sh` | Process Management | ps, kill, jobs, signals |
| `08-network-utilities.sh` | Network Utilities | ping, wget, curl, netstat |
| `09-shell-scripting.sh` | Shell Scripting | Script creation, functions, loops |
| `master-demo.sh` | All Sections | Interactive menu for all demos |

### Running Individual Demos

```bash
# Enter main container
docker exec -it unix-linux-demo bash

# Run specific demo
cd /demo
bash scripts/01-getting-started.sh

# Or run with execution permission
chmod +x scripts/02-file-management.sh
./scripts/02-file-management.sh
```

### Running All Demos Sequentially

```bash
# Interactive mode (recommended)
bash scripts/master-demo.sh

# Automated mode (non-interactive)
for script in scripts/0*.sh; do
    echo "Running $script..."
    bash "$script"
    echo "Press Enter to continue..."
    read
done
```

## Directory Structure and File Locations

```
/Users/lap16470/Cole/Demo/D8 - Unix:Linux/
├── docker-compose.yml          # Main orchestration file
├── README.md                   # Original presentation content
├── DEMO-GUIDE.md              # This guide
├── demo-scripts/               # All demonstration scripts
│   ├── 01-getting-started.sh
│   ├── 02-file-management.sh
│   ├── ... (all demo scripts)
│   └── master-demo.sh
├── demo-data/                  # Persistent data directory
│   └── (files created during demos)
├── demo-logs/                  # Log files from log-generator
│   ├── app.log
│   └── access.log
├── demo-backup/                # Backup destination directory
├── web-content/                # Web server content
│   ├── index.html
│   ├── demo-data.json
│   ├── demo-text.txt
│   └── demo-config.conf
└── ftp-data/                   # FTP server data directory
    └── (FTP accessible files)
```

### Container Internal Paths

**Main Container (`unix-linux-demo`)**:
```
/demo/
├── scripts/                    # Demo scripts (read-only)
├── data/                      # Working data directory
├── logs/                      # Log files
└── backup/                    # Backup directory
```

## Comprehensive Demo Scenarios

### Scenario 1: Basic Unix/Linux Skills

**Objective**: Learn fundamental commands and concepts

**Steps**:
1. Start with getting started demo
2. Practice file management operations
3. Explore directory navigation
4. Understand file permissions
5. Configure environment variables

**Commands**:
```bash
docker exec -it unix-linux-demo bash
cd /demo
bash scripts/01-getting-started.sh
bash scripts/02-file-management.sh
bash scripts/03-directory-management.sh
bash scripts/04-file-permissions.sh
bash scripts/05-environment.sh
```

### Scenario 2: Text Processing and Data Analysis

**Objective**: Master pipes, filters, and data processing

**Steps**:
1. Generate sample data
2. Practice grep patterns
3. Use awk for data analysis
4. Create processing pipelines
5. Analyze real log files

**Commands**:
```bash
cd /demo
bash scripts/06-pipes-filters.sh

# Additional practice
tail -f logs/app.log | grep "ERROR"
awk '/ERROR/ {count++} END {print "Errors:", count}' logs/app.log
grep "User login" logs/access.log | cut -d' ' -f5 | sort | uniq -c
```

### Scenario 3: System Administration

**Objective**: Learn process and network management

**Steps**:
1. Monitor system processes
2. Control background jobs
3. Test network connectivity
4. Download files from web server
5. Analyze system performance

**Commands**:
```bash
bash scripts/07-process-management.sh
bash scripts/08-network-utilities.sh

# Additional system admin tasks
ps aux | sort -k3 -nr | head -10  # Top CPU users
netstat -tuln | grep LISTEN       # Listening ports
curl -I http://web-server/         # HTTP headers
ping -c 5 db-server               # Database connectivity
```

### Scenario 4: Automation and Scripting

**Objective**: Create automated solutions

**Steps**:
1. Learn script structure
2. Practice variables and functions
3. Implement conditional logic
4. Create useful utilities
5. Automate repetitive tasks

**Commands**:
```bash
bash scripts/09-shell-scripting.sh

# Create custom automation
cat > /demo/data/system-monitor.sh << 'EOF'
#!/bin/bash
while true; do
    echo "=== $(date) ==="
    echo "Load: $(uptime | cut -d, -f3-)"
    echo "Processes: $(ps aux | wc -l)"
    echo "Disk: $(df / | tail -1 | awk '{print $5}')"
    sleep 10
done
EOF

chmod +x /demo/data/system-monitor.sh
./system-monitor.sh
```

## Advanced Usage Scenarios

### Network Services Integration

**Multi-container Testing**:
```bash
# Test all services from main container
docker exec -it unix-linux-demo bash

# Web server testing
curl -s http://web-server/ | grep -o '<title>.*</title>'
wget -q -O - http://web-server/demo-data.json | head -10

# Database connectivity
nc -z db-server 3306 && echo "Database reachable"

# FTP server testing
echo "ls" | ftp -n ftp-server # (requires manual login)
```

### Log Analysis Workshop

**Real-time Log Processing**:
```bash
# Terminal 1: Generate logs
docker exec -it demo-logger bash

# Terminal 2: Analyze logs
docker exec -it unix-linux-demo bash
cd /demo/logs

# Monitor error patterns
tail -f app.log | grep --color "ERROR"

# Count log levels
awk '{print $3}' app.log | sort | uniq -c

# Find peak activity times
awk '{print $2}' access.log | cut -d: -f1-2 | sort | uniq -c | sort -nr
```

### System Monitoring Dashboard

**Create Live Monitoring**:
```bash
# Create monitoring script
cat > /demo/data/dashboard.sh << 'EOF'
#!/bin/bash
while true; do
    clear
    echo "=== SYSTEM DASHBOARD ==="
    echo "Time: $(date)"
    echo
    echo "=== CONTAINERS ==="
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    echo
    echo "=== NETWORK TESTS ==="
    ping -c 1 web-server >/dev/null && echo "✓ Web Server" || echo "✗ Web Server"
    ping -c 1 db-server >/dev/null && echo "✓ Database" || echo "✗ Database"
    ping -c 1 ftp-server >/dev/null && echo "✓ FTP Server" || echo "✗ FTP Server"
    echo
    echo "=== LOG SUMMARY ==="
    echo "App Errors: $(grep -c ERROR /demo/logs/app.log 2>/dev/null || echo 0)"
    echo "Access Entries: $(wc -l < /demo/logs/access.log 2>/dev/null || echo 0)"
    sleep 5
done
EOF

chmod +x /demo/data/dashboard.sh
./dashboard.sh
```

## Troubleshooting Guide

### Common Issues and Solutions

**Issue**: Containers not starting
```bash
# Check Docker daemon
docker --version
docker-compose --version

# Check port conflicts
netstat -tuln | grep -E "(8080|21|3000[0-9])"

# Reset environment
docker-compose down -v
docker-compose up -d
```

**Issue**: Permission denied errors
```bash
# Fix permissions
docker exec -it unix-linux-demo bash
chown -R demouser:demouser /demo/data
chmod +x /demo/scripts/*.sh
```

**Issue**: Network connectivity problems
```bash
# Check network
docker network ls
docker network inspect d8-unixlinux_demo-network

# Test internal connectivity
docker exec -it unix-linux-demo ping web-server
docker exec -it unix-linux-demo nc -z db-server 3306
```

**Issue**: Scripts not executing
```bash
# Make scripts executable
chmod +x /demo/scripts/*.sh

# Check script syntax
bash -n /demo/scripts/master-demo.sh

# Run with debug output
bash -x /demo/scripts/01-getting-started.sh
```

### Performance Optimization

**Resource Monitoring**:
```bash
# Check container resource usage
docker stats

# Monitor logs size
du -sh /demo/logs/

# Clean up old files
find /demo/data -name "*.tmp" -delete
find /demo/backup -mtime +7 -delete
```

**Memory Management**:
```bash
# Inside main container
free -h
ps aux --sort=-%mem | head -10

# Clean up if needed
echo 3 > /proc/sys/vm/drop_caches  # (if running as root)
```

## Educational Objectives and Learning Outcomes

### By Section Completion

**Getting Started (Script 01)**:
- ✅ Understand basic Unix/Linux commands
- ✅ Navigate help systems effectively
- ✅ Comprehend command structure
- ✅ Execute basic system queries

**File Management (Script 02)**:
- ✅ Create and manipulate files
- ✅ Use various file viewing methods
- ✅ Copy and move files safely
- ✅ Understand file properties

**Directory Management (Script 03)**:
- ✅ Navigate directory structures
- ✅ Create and organize directories
- ✅ Use listing and search commands
- ✅ Understand directory permissions

**File Permissions (Script 04)**:
- ✅ Read permission notation
- ✅ Modify file permissions
- ✅ Understand security implications
- ✅ Use umask effectively

**Environment (Script 05)**:
- ✅ Configure environment variables
- ✅ Create and use aliases
- ✅ Understand shell configuration
- ✅ Manage command history

**Pipes and Filters (Script 06)**:
- ✅ Build command pipelines
- ✅ Use text processing tools
- ✅ Analyze data with Unix tools
- ✅ Create complex filters

**Process Management (Script 07)**:
- ✅ Monitor system processes
- ✅ Control background jobs
- ✅ Understand signal handling
- ✅ Manage system resources

**Network Utilities (Script 08)**:
- ✅ Test network connectivity
- ✅ Download files programmatically
- ✅ Analyze network configuration
- ✅ Troubleshoot network issues

**Shell Scripting (Script 09)**:
- ✅ Write effective shell scripts
- ✅ Use variables and functions
- ✅ Implement control structures
- ✅ Create automation tools

## Additional Resources and Extensions

### Extended Learning Paths

**System Administration Track**:
1. Complete all basic demos
2. Practice log analysis with real data
3. Create monitoring scripts
4. Implement backup strategies
5. Set up automated maintenance

**DevOps Track**:
1. Master shell scripting
2. Learn container management
3. Practice network troubleshooting
4. Implement CI/CD concepts
5. Create deployment scripts

**Security Track**:
1. Focus on file permissions
2. Practice user management
3. Learn process isolation
4. Understand network security
5. Implement security auditing

### Customization Options

**Add New Services**:
```yaml
# Add to docker-compose.yml
redis-server:
  image: redis:alpine
  container_name: demo-redis
  networks:
    - demo-network
```

**Custom Demo Scripts**:
```bash
# Create specialized demos
cat > /demo/scripts/10-custom-demo.sh << 'EOF'
#!/bin/bash
echo "=== Custom Demo ==="
# Your custom demonstration here
EOF
```

**Extended Data Sets**:
```bash
# Generate larger test files
seq 1 10000 > /demo/data/large_numbers.txt
curl -s "https://jsonplaceholder.typicode.com/posts" > /demo/data/api_data.json
```

## Cleanup and Maintenance

### Regular Cleanup

```bash
# Stop and remove containers
docker-compose down

# Remove all data (WARNING: destructive)
docker-compose down -v
rm -rf demo-data/* demo-logs/* demo-backup/*

# Clean Docker resources
docker system prune -f
docker volume prune -f
```

### Backup Important Work

```bash
# Backup custom scripts and data
tar -czf unix-demo-backup-$(date +%Y%m%d).tar.gz \
    demo-data/ demo-scripts/ demo-backup/

# Backup specific container data
docker exec unix-linux-demo tar -czf /demo/backup/container-backup.tar.gz /demo/data
```

### Reset to Initial State

```bash
# Complete reset
docker-compose down -v
docker-compose pull
docker-compose up -d

# Wait for initialization
sleep 30

# Verify reset
docker exec -it unix-linux-demo bash -c "ls -la /demo"
```

## Support and Troubleshooting Contacts

### Documentation Sources
- Main README.md: Complete Unix/Linux reference
- Docker Compose documentation: https://docs.docker.com/compose/
- Ubuntu documentation: https://help.ubuntu.com/

### Common Commands Reference
```bash
# Container management
docker-compose up -d          # Start all services
docker-compose down           # Stop all services
docker-compose logs           # View all logs
docker-compose ps             # Check service status

# Access containers
docker exec -it unix-linux-demo bash     # Main demo container
docker exec -it demo-webserver sh        # Web server (Alpine)
docker exec -it demo-database bash       # Database container

# Network testing
docker network ls                         # List networks
docker network inspect <network_name>    # Network details
```

This comprehensive demo environment provides hands-on experience with all Unix/Linux concepts covered in the presentation, from basic commands to advanced system administration and automation techniques.
