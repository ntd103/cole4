#!/bin/bash

# DuckDB Demo Quick Setup Script
# ==============================
# This script sets up the complete DuckDB demonstration environment

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Banner
echo "🦆 DuckDB Performance Demo Setup"
echo "================================="
echo

# Check prerequisites
print_status "Checking prerequisites..."

# Check Docker
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

print_success "Docker and Docker Compose are available"

# Check system resources
TOTAL_RAM=$(free -g | awk '/^Mem:/{print $2}')
if [ "$TOTAL_RAM" -lt 6 ]; then
    print_warning "System has ${TOTAL_RAM}GB RAM. 8GB+ recommended for optimal performance."
fi

AVAILABLE_SPACE=$(df . | tail -1 | awk '{print int($4/1024/1024)}')
if [ "$AVAILABLE_SPACE" -lt 5 ]; then
    print_warning "Available disk space: ${AVAILABLE_SPACE}GB. 5GB+ recommended."
fi

# Create project structure
print_status "Creating project structure..."

mkdir -p {notebooks,data,scripts}

print_success "Project directories created"

# Create docker-compose.yml
print_status "Creating Docker configuration..."

cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  jupyter:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8888:8888"
    volumes:
      - ./notebooks:/home/jovyan/work
      - ./data:/home/jovyan/data
      - ./scripts:/home/jovyan/scripts
    environment:
      - JUPYTER_ENABLE_LAB=yes
      - JUPYTER_TOKEN=duckdb-demo
    command: start-notebook.sh --NotebookApp.token='duckdb-demo' --NotebookApp.password=''

  data-generator:
    build:
      context: .
      dockerfile: Dockerfile.datagen
    volumes:
      - ./data:/app/data
    command: python generate_sample_data.py

volumes:
  data:
  notebooks:
EOF

# Create Dockerfiles
print_status "Creating Dockerfile for Jupyter..."

cat > Dockerfile << 'EOF'
FROM jupyter/scipy-notebook:latest

USER root

RUN apt-get update && apt-get install -y \
    wget \
    curl \
    vim \
    htop \
    && rm -rf /var/lib/apt/lists/*

USER $NB_UID

RUN pip install --no-cache-dir \
    duckdb==0.9.2 \
    pandas==2.1.4 \
    pyarrow==14.0.1 \
    plotly==5.17.0 \
    seaborn==0.13.0 \
    faker==20.1.0 \
    memory-profiler==0.61.0 \
    psutil==5.9.6 \
    tqdm==4.66.1 \
    jupyter-lab==4.0.9 \
    ipywidgets==8.1.1

WORKDIR /home/jovyan
RUN mkdir -p work data scripts

EXPOSE 8888
EOF

cat > Dockerfile.datagen << 'EOF'
FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    pandas==2.1.4 \
    faker==20.1.0 \
    numpy==1.24.3 \
    pyarrow==14.0.1 \
    tqdm==4.66.1

COPY generate_sample_data.py /app/
RUN mkdir -p /app/data

CMD ["python", "generate_sample_data.py"]
EOF

# Create Makefile
print_status "Creating Makefile..."

cat > Makefile << 'EOF'
.PHONY: help build up down logs clean data notebook shell

help:
	@echo "DuckDB Demo Commands:"
	@echo "  make up        - Start demo environment"
	@echo "  make down      - Stop services"
	@echo "  make data      - Generate sample data"
	@echo "  make notebook  - Open Jupyter in browser"
	@echo "  make logs      - View logs"
	@echo "  make clean     - Clean everything"

build:
	docker-compose build

up: build
	@echo "🚀 Starting DuckDB demo..."
	docker-compose up -d
	@echo "✅ Demo started at http://localhost:8888"
	@echo "🔑 Token: duckdb-demo"
	@sleep 5
	@make data

down:
	docker-compose down

data:
	@echo "📊 Generating data..."
	docker-compose run --rm data-generator

notebook:
	@if command -v open >/dev/null 2>&1; then \
		open http://localhost:8888; \
	elif command -v xdg-open >/dev/null 2>&1; then \
		xdg-open http://localhost:8888; \
	else \
		echo "Open: http://localhost:8888"; \
	fi

logs:
	docker-compose logs -f

shell:
	docker-compose exec jupyter bash

clean:
	docker-compose down -v
	docker system prune -f
EOF

# Check if generate_sample_data.py exists, create a minimal version if not
if [ ! -f "generate_sample_data.py" ]; then
    print_status "Creating data generation script..."
    
    cat > generate_sample_data.py << 'EOF'
#!/usr/bin/env python3
"""Minimal data generator for DuckDB demo"""

import pandas as pd
import numpy as np
from faker import Faker
import os
from datetime import datetime, timedelta
import random
from tqdm import tqdm

np.random.seed(42)
fake = Faker()
Faker.seed(42)

def generate_sample_data():
    print("🦆 Generating DuckDB demo data...")
    
    os.makedirs('/app/data', exist_ok=True)
    
    # Generate smaller datasets for quick demo
    print("Generating transactions...")
    transactions = []
    for i in tqdm(range(100000)):  # 100K transactions
        transactions.append({
            'transaction_id': i + 1,
            'customer_id': random.randint(1, 10000),
            'transaction_date': fake.date_between(start_date='-1y', end_date='today'),
            'product_category': random.choice(['Electronics', 'Clothing', 'Books', 'Food']),
            'total_amount': round(random.uniform(10, 500), 2),
            'quantity': random.randint(1, 5)
        })
    
    df_transactions = pd.DataFrame(transactions)
    df_transactions.to_parquet('/app/data/transactions.parquet', index=False)
    print(f"✅ Generated {len(df_transactions):,} transactions")
    
    # Generate customers
    print("Generating customers...")
    customers = []
    for i in tqdm(range(10000)):  # 10K customers
        customers.append({
            'customer_id': i + 1,
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'customer_segment': random.choice(['Premium', 'Standard', 'Basic']),
            'annual_income': random.randint(30000, 120000)
        })
    
    df_customers = pd.DataFrame(customers)
    df_customers.to_parquet('/app/data/customers.parquet', index=False)
    print(f"✅ Generated {len(df_customers):,} customers")
    
    print("🎉 Sample data generation complete!")

if __name__ == "__main__":
    generate_sample_data()
EOF
    
    print_success "Created data generation script"
fi

# Make files executable
chmod +x generate_sample_data.py

# Create sample notebook if it doesn't exist
if [ ! -f "notebooks/demo.ipynb" ]; then
    print_status "Creating sample notebook..."
    
    mkdir -p notebooks
    cat > notebooks/demo.ipynb << 'EOF'
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# DuckDB Demo Notebook\n",
    "\n",
    "Welcome to the DuckDB performance demonstration!"