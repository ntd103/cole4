#!/bin/bash

# Hadoop Ecosystem Demo - Startup Script
# This script helps students start the entire Hadoop ecosystem environment

echo "==============================================="
echo "Hadoop Ecosystem Demo - Environment Startup"
echo "==============================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "✅ Docker is running"

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed. Please install docker-compose first."
    exit 1
fi

echo "✅ docker-compose is available"

# Function to check if a service is healthy
check_service_health() {
    local service_name=$1
    local max_attempts=30
    local attempt=1
    
    echo "🔍 Checking $service_name health..."
    
    while [ $attempt -le $max_attempts ]; do
        if docker-compose ps | grep "$service_name" | grep -q "Up"; then
            echo "✅ $service_name is healthy"
            return 0
        fi
        
        echo "⏳ Waiting for $service_name... (attempt $attempt/$max_attempts)"
        sleep 10
        attempt=$((attempt + 1))
    done
    
    echo "❌ $service_name failed to start properly"
    return 1
}

# Start the environment
echo ""
echo "🚀 Starting Hadoop Ecosystem Environment..."
echo "This may take several minutes on first run..."
echo ""

# Pull latest images and start services
docker-compose pull
docker-compose up -d

# Wait for core services to be ready
echo ""
echo "⏳ Waiting for services to initialize..."
echo ""

# Check core services
services=("namenode" "datanode" "resourcemanager" "nodemanager" "hive-server" "hbase-master" "mysql" "jupyter")

for service in "${services[@]}"; do
    if ! check_service_health "$service"; then
        echo "❌ Failed to start $service. Check logs with: docker-compose logs $service"
        echo "Continuing with other services..."
    fi
done

# Display service status
echo ""
echo "📊 Service Status:"
echo "=================="
docker-compose ps

# Check and display web interfaces
echo ""
echo "🌐 Web Interface URLs:"
echo "====================="

# Function to check if a port is responding
check_port() {
    local port=$1
    local name=$2
    local url=$3
    
    if curl -s "http://localhost:$port" > /dev/null 2>&1; then
        echo "✅ $name: $url"
    else
        echo "❌ $name: $url (not responding)"
    fi
}

check_port 9870 "HDFS NameNode" "http://localhost:9870"
check_port 8088 "YARN ResourceManager" "http://localhost:8088"
check_port 16010 "HBase Master" "http://localhost:16010"
check_port 8888 "Jupyter Notebook" "http://localhost:8888 (token: hadoop)"

# Additional service checks
echo ""
echo "🔧 Service Connection Tests:"
echo "============================"

# Test HDFS
echo -n "HDFS: "
if docker exec -it namenode hdfs dfs -ls / > /dev/null 2>&1; then
    echo "✅ Ready"
else
    echo "❌ Not responding"
fi

# Test Hive
echo -n "Hive: "
if docker exec -it hive-server sh -c 'beeline -u jdbc:hive2://localhost:10000 -e "SHOW DATABASES;" --silent=true' > /dev/null 2>&1; then
    echo "✅ Ready"
else
    echo "❌ Not responding"
fi

# Test HBase
echo -n "HBase: "
if docker exec -it hbase-master sh -c 'echo "status" | hbase shell' > /dev/null 2>&1; then
    echo "✅ Ready"
else
    echo "❌ Not responding"
fi

# Test MySQL
echo -n "MySQL: "
if docker exec -it mysql mysql -u sqoop -psqoop -e "SHOW DATABASES;" > /dev/null 2>&1; then
    echo "✅ Ready"
else
    echo "❌ Not responding"
fi

# Display useful commands
echo ""
echo "📋 Useful Commands:"
echo "=================="
echo "• Check all services: docker-compose ps"
echo "• View logs: docker-compose logs [service-name]"
echo "• Stop environment: docker-compose down"
echo "• Access HDFS: docker exec -it namenode bash"
echo "• Access Hive: docker exec -it hive-server bash"
echo "• Access HBase: docker exec -it hbase-master bash"
echo "• Access MySQL: docker exec -it mysql mysql -u sqloop -psqloop testdb"

# Setup instructions
echo ""
echo "🎯 Next Steps:"
echo "============="
echo "1. Access Jupyter Notebook at http://localhost:8888 (token: hadoop)"
echo "2. Open the hadoop_ecosystem_demo.ipynb notebook"
echo "3. Start with Exercise 1: HDFS Basics"
echo "4. Follow the progressive exercises 1 through 5"
echo ""
echo "📚 Exercise Structure:"
echo "• Exercise 1: HDFS Basics (Beginner)"
echo "• Exercise 2: Hive Data Warehousing (Intermediate)"
echo "• Exercise 3: HBase NoSQL Operations (Intermediate)"
echo "• Exercise 4: Data Integration with Sqoop (Advanced)"
echo "• Exercise 5: Python Integration and Pipeline (Advanced)"

# Troubleshooting tips
echo ""
echo "🔧 Troubleshooting:"
echo "=================="
echo "• If services fail to start, try: docker-compose down && docker-compose up -d"
echo "• For memory issues, increase Docker memory allocation to at least 8GB"
echo "• Check logs for specific errors: docker-compose logs [service-name]"
echo "• Restart individual services: docker-compose restart [service-name]"
echo ""
echo "✨ Environment startup complete! Happy learning!"
echo "==============================================="
