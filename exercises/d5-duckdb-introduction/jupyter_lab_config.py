#!/usr/bin/env python3

c = get_config()

# Network settings
c.ServerApp.ip = '0.0.0.0'
c.ServerApp.port = 8888
c.ServerApp.open_browser = False
c.ServerApp.allow_root = True

# Security settings
c.ServerApp.token = 'duckdb-demo'
c.ServerApp.password = ''
c.ServerApp.disable_check_xsrf = True

# Directory settings
c.ServerApp.notebook_dir = '/home/jovyan/work'
c.ServerApp.allow_remote_access = True

# Enable extensions
c.ServerApp.jpserver_extensions = {
    'jupyterlab': True,
}

# Resource limits
c.ResourceUseDisplay.mem_limit = 8 * 1024**3  # 8GB
c.ResourceUseDisplay.track_cpu_percent = True