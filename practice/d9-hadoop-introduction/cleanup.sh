#!/bin/bash

# Clean shutdown script for Hadoop cluster
echo "Shutting down Hadoop cluster..."

# Stop all containers
docker-compose down

# Remove containers and networks
docker-compose down --remove-orphans

# Optional: Remove volumes (uncomment if you want to clean all data)
# docker-compose down -v

echo "Hadoop cluster stopped successfully."
echo "To remove all data, run: docker-compose down -v"
