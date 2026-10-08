FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY cat_analyzer.py .

# Create data directory
RUN mkdir -p /app/data

# Create non-root user for security
RUN useradd -m -u 1000 catuser && chown -R catuser:catuser /app
USER catuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('https://catfact.ninja/fact', timeout=5)" || exit 1

# Run the application
CMD ["python", "cat_analyzer.py"]