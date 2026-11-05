.PHONY: help build up down logs clean data notebook shell wait reset status dev-logs dev-restart

# /dev/tcp needs bash, not dash
SHELL := /bin/bash
COMPOSE := docker compose

help:
	@echo "DuckDB Demo Environment"
	@echo "======================"
	@echo ""
	@echo "  make build     - Build images (only when Dockerfile* changed)"
	@echo "  make up        - Start services (no rebuild) + data if missing"
	@echo "  make down      - Stop services"
	@echo "  make data      - Generate sample data (FORCE=1 to regenerate)"
	@echo "  make notebook  - Open Jupyter Lab in browser"
	@echo "  make logs      - Follow container logs"
	@echo "  make shell     - Shell into Jupyter container"
	@echo "  make status    - Container + data status"
	@echo "  make clean     - Remove containers and volumes"
	@echo "  make reset     - Clean + rebuild from scratch"
	@echo ""
	@echo "First run on fresh clone: make build && make up"

build:
	@echo "🔨 Building images..."
	$(COMPOSE) build

# no longer depends on build: images rarely change, `up` should be instant
up:
	@echo "🚀 Starting..."
	$(COMPOSE) up -d
	@$(MAKE) --no-print-directory wait
	@echo "✅ Jupyter Lab: http://localhost:8888  (token: duckdb-demo)"
	@$(MAKE) --no-print-directory data

# poll the port instead of a blind `sleep 10`
wait:
	@printf "⏳ Waiting for Jupyter"
	@for i in $$(seq 1 60); do \
		(exec 3<>/dev/tcp/127.0.0.1/$${JUPYTER_PORT:-8888}) 2>/dev/null && { echo " ready"; exit 0; }; \
		printf "."; sleep 1; \
	done; echo " ❌ not ready after 60s"; exit 1

down:
	@echo "🛑 Stopping..."
	$(COMPOSE) down

# idempotent: generation is the expensive part, don't redo it on every `up`
data:
	@if [ -f data/transactions.parquet ] && [ -z "$(FORCE)" ]; then \
		echo "📦 data/ already populated (FORCE=1 make data to regenerate)"; \
	else \
		echo "📊 Generating sample data..."; \
		$(COMPOSE) run --rm data-generator; \
	fi

notebook:
	@if command -v open >/dev/null 2>&1; then open http://localhost:8888; \
	elif command -v xdg-open >/dev/null 2>&1; then xdg-open http://localhost:8888; \
	else echo "Open http://localhost:8888  (token: duckdb-demo)"; fi

logs:
	$(COMPOSE) logs -f

shell:
	$(COMPOSE) exec jupyter bash

clean:
	@echo "🧹 Cleaning..."
	$(COMPOSE) down -v
	docker system prune -f

reset: clean
	@echo "🔄 Full reset..."
	$(COMPOSE) build --no-cache
	@$(MAKE) --no-print-directory up

dev-logs:
	$(COMPOSE) logs -f jupyter

dev-restart:
	$(COMPOSE) restart jupyter

status:
	@echo "📋 Containers:"
	@$(COMPOSE) ps
	@echo ""
	@echo "📊 Data:"
	@if [ -d ./data ]; then ls -la ./data/; \
	else echo "No data dir. Run 'make data'."; fi