#!/bin/bash

echo "========================================="
echo "Fixing Hive Metastore Schema Issues"
echo "========================================="

# Stop the problematic services
echo "Stopping Hive services..."
docker-compose stop hive-server2 hive-metastore

# Wait a bit
sleep 5

# Remove the metastore container to force recreation
echo "Removing Hive Metastore container..."
docker-compose rm -f hive-metastore

# Initialize the schema manually
echo "Initializing Hive Metastore schema..."
docker-compose run --rm hive-metastore /opt/hive/bin/schematool -initSchema -dbType postgres

# Start the services again
echo "Starting Hive services..."
docker-compose up -d hive-metastore

# Wait for metastore to be ready
echo "Waiting for Hive Metastore to be ready..."
sleep 30

# Start Hive Server2
docker-compose up -d hive-server2

echo "========================================="
echo "Hive Metastore fix completed!"
echo "Check logs with: docker-compose logs hive-metastore"
echo "========================================="
