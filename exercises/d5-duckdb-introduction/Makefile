.PHONY: help build up down logs clean data notebook shell

# Default target
help:
	@echo "DuckDB Demo Environment"
	@echo "======================"
	@echo ""
	@echo "Available commands:"
	@echo "  make build     - Build Docker images"
	@echo "  make up        - Start all services"
	@echo "  make down      - Stop all services"
	@echo "  make data      - Generate sample data"
	@echo "  make notebook  - Open Jupyter notebook"
	@echo "  make logs      - View container logs"
	@echo "  make shell     - Access Jupyter container shell"
	@echo "  make clean     - Clean up containers and volumes"
	@echo "  make reset     - Full reset (clean + rebuild)"
	@echo ""

# Build Docker images
build:
	@echo "🔨 Building Docker images..."
	docker-compose build

# Start services
up: build
	@echo "🚀 Starting DuckDB demo environment..."
	docker-compose up -d
	@echo ""
	@echo "✅ Services started!"
	@echo "📊 Jupyter Lab: http://localhost:8888"
	@echo "🔑 Token: duckdb-demo"
	@echo ""
	@echo "Waiting for services to be ready..."
	@sleep 10
	@make data

# Stop services
down:
	@echo "🛑 Stopping services..."
	docker-compose down

# Generate sample data
data:
	@echo "📊 Generating sample data..."
	docker-compose run --rm data-generator
	@echo "✅ Sample data generated!"

# Open notebook in browser (macOS/Linux)
notebook:
	@echo "🌐 Opening Jupyter Lab..."
	@if command -v open >/dev/null 2>&1; then \
		open http://localhost:8888; \
	elif command -v xdg-open >/dev/null 2>&1; then \
		xdg-open http://localhost:8888; \
	else \
		echo "📋 Please open: http://localhost:8888"; \
		echo "🔑 Token: duckdb-demo"; \
	fi

# View logs
logs:
	docker-compose logs -f

# Access container shell
shell:
	docker-compose exec jupyter bash

# Clean up
clean:
	@echo "🧹 Cleaning up..."
	docker-compose down -v
	docker system prune -f

# Full reset
reset: clean
	@echo "🔄 Full reset..."
	docker-compose build --no-cache
	@make up

# Development commands
dev-logs:
	docker-compose logs -f jupyter

dev-restart:
	docker-compose restart jupyter

# Check status
status:
	@echo "📋 Service Status:"
	@docker-compose ps
	@echo ""
	@echo "📊 Data Status:"
	@if [ -d "./data" ]; then \
		ls -la ./data/; \
	else \
		echo "No data directory found. Run 'make data' to generate."; \
	fi