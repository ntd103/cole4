#!/bin/bash

# Convenience script to run the demo

echo "🚀 Starting Spark Demo Environment..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Create directories
mkdir -p data/csv data/json data/parquet notebooks sql

# Generate sample data
echo "📊 Generating sample data..."
python3 scripts/generate_sample_data.py

# Start Docker Compose
echo "🐳 Starting Docker containers..."
docker-compose up -d

echo "⏳ Waiting for services to start..."
sleep 30

# Run the basic demo
echo "🎯 Running Spark demo..."
docker exec spark-master python3 /home/spark/scripts/spark_demo_basic.py

echo "✅ Demo completed!"
echo ""
echo "🌐 Access points:"
echo "  - Spark Master UI: http://localhost:8080"
echo "  - Jupyter Lab: http://localhost:8889 (password: jupyter)"
echo "  - PostgreSQL: localhost:5432 (user: spark, password: sparkpassword)"
echo ""
echo "🛑 To stop the demo:"
echo "  docker-compose down"