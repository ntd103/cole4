FROM python:3.9-slim

# Install Java (required for Hadoop client)
RUN apt-get update && apt-get install -y \
    default-jdk \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/default-java

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# Copy Hadoop configuration
COPY hadoop-conf /app/hadoop-conf

# Copy Python scripts
COPY . /app

# Create directories for data
RUN mkdir -p /data /exercises

CMD ["tail", "-f", "/dev/null"]
