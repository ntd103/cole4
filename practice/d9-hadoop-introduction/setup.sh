#!/bin/bash

# Hadoop/HDFS Demo Setup Script
echo "Setting up Hadoop/HDFS Demo Environment..."

# Check if Docker and Docker Compose are installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "Error: Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
echo "Creating data directories..."
mkdir -p data logs

# Set permissions for data directories
chmod 755 data logs

# Start the Hadoop cluster
echo "Starting Hadoop cluster..."
docker-compose up -d

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 30

# Check if Namenode is running
echo "Checking Namenode status..."
docker exec hadoop-namenode hdfs dfsadmin -report || echo "Namenode still starting up..."

# Check if HDFS Web UI is accessible
echo "HDFS Web UI should be available at: http://localhost:9870"
echo "Datanode Web UI should be available at: http://localhost:9864"

# Enter Python client container
echo "Setup complete! You can now run exercises."
echo "To enter the Python client container, run:"
echo "docker exec -it hadoop-python-client bash"

echo "To run the demo:"
echo "docker exec -it hadoop-python-client python /app/hdfs_demo.py"
