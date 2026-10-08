# 🐱 Cat Fact Analyzer - Docker Demo

A hilariously over-engineered application that demonstrates Docker and Docker Compose by analyzing cat facts with scientific rigor.

## What This Demo Shows

- **Docker fundamentals**: Containerizing a Python application
- **Docker Compose**: Multi-service orchestration
- **Best practices**: Multi-stage builds, non-root users, health checks
- **Real-world example**: Web scraping, data analysis, and web interface

## Quick Start

1. **Clone and run the demo:**
   ```bash
   # Make sure you have Docker and Docker Compose installed
   docker-compose up --build
   ```

2. **View the results:**
   - Main analysis: Check the console output
   - Web interface: Visit http://localhost:8080
   - Logs: `docker-compose logs cat-analyzer`

3. **Stop the demo:**
   ```bash
   docker-compose down
   ```

## What It Does

The Cat Fact Analyzer performs "scientific research" by:
- 🌐 Crawling cat facts from a public API
- 📊 Analyzing text patterns with pandas
- 🎯 Calculating ridiculous metrics like "cuteness factor"
- 📈 Providing statistical insights about feline knowledge
- 🌐 Serving results via a web interface

## Architecture

- **cat-analyzer**: Main Python application (console output)
- **cat-web**: Flask web interface (http://localhost:8080)
- **Networking**: Services communicate via Docker network
- **Data persistence**: Optional volume mounting for data

## Files Structure

```
├── docker-compose.yml      # Multi-service orchestration
├── Dockerfile             # Main app container
├── Dockerfile.web         # Web interface container
├── cat_analyzer.py        # Main analysis application
├── web_app.py            # Flask web interface
├── requirements.txt       # Python dependencies
├── requirements.web.txt   # Web app dependencies
├── templates/index.html   # Web interface template
└── .dockerignore         # Docker ignore rules
```

Perfect for demonstrating Docker concepts while having fun with data! 🐾