#!/bin/bash

# Spark Deep Dive Demo Startup Script
echo "🚀 Starting Spark Deep Dive Demo Environment"
echo "=============================================="

# Start Docker Compose services
echo "Starting Docker services..."
docker-compose up -d

# Wait for services to be ready
echo "Waiting for services to initialize..."
sleep 30

# Check service status
echo ""
echo "Service Status:"
echo "==============="
docker-compose ps

echo ""
echo "🌐 Access URLs:"
echo "==============="
echo "Spark Master Web UI: http://localhost:8080"
echo "Jupyter Notebook: http://localhost:8889 (token: 123456)"
echo "PostgreSQL: localhost:5432 (user: spark, password: sparkpassword)"

echo ""
echo "📁 Demo Structure:"
echo "=================="
echo "notebooks/ - Jupyter notebooks with demos"
echo "data/ - Sample datasets"
echo "scripts/ - Utility scripts"
echo "sql/ - Database initialization scripts"

echo ""
echo "🎯 Demo Notebooks Available:"
echo "============================"
echo "1. spark_deep_dive_demo.ipynb - Main comprehensive demo"
echo "2. catalyst_optimizer_demo.ipynb - Catalyst optimizer deep dive"
echo "3. memory_performance_tuning.ipynb - Memory management and tuning"

echo ""
echo "💡 Quick Start:"
echo "==============="
echo "1. Open Jupyter at http://localhost:8889"
echo "2. Use token: 123456"
echo "3. Navigate to work/ directory"
echo "4. Start with spark_deep_dive_demo.ipynb"

echo ""
echo "✅ Environment is ready!"
