FROM jupyter/scipy-notebook:latest

USER root

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    vim \
    htop \
    && rm -rf /var/lib/apt/lists/*

USER $NB_UID

# Install Python packages
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
    ipywidgets==8.1.1 \
    nbconvert==7.12.0

# Install JupyterLab extensions
RUN pip install --no-cache-dir \
    jupyterlab-git \
    jupyterlab-code-formatter

# Set working directory
WORKDIR /home/jovyan

# Create directories
RUN mkdir -p work data scripts

# Copy configuration files
COPY --chown=$NB_UID:$NB_GID jupyter_lab_config.py /home/jovyan/.jupyter/

# Expose port
EXPOSE 8888