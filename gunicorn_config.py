# gunicorn_config.py

# Worker Class:
# Using 'gevent' for asynchronous workloads. 
# Ensure gevent is installed: pip install gevent
worker_class = 'gevent'

# Number of Workers:
# A conservative number of workers considering the Raspberry Pi's resources and your application's complexity.
# Adjust based on performance and resource usage.
workers = 2

# Threads:
# The number of threads per worker process. 
# Since you have external threads, keep this low to avoid overloading the Raspberry Pi.
threads = 2

# Worker Connections:
# The maximum number of simultaneous clients for each worker. Relevant for gevent or eventlet workers.
worker_connections = 1000

# Bind Address:
# Binding to all IPs on port 8000.
bind = '0.0.0.0:8000'

# Timeout:
# Adjust as necessary based on your application's requirements.
timeout = 30

# Keep Alive:
# Duration to keep a Keep-Alive type connection open.
keepalive = 2

# Logging:
# Paths for access and error logs.
accesslog = '/home/izitto/Documents/Code/PAtDS/static/g-logs/access.log'
errorlog = '/home/izitto/Documents/Code/PAtDS/static/g-logs/error.log'

# Log Level:
# Adjust the log level as needed. Options include debug, info, warning, error, and critical.
loglevel = 'info'

# Daemon Mode:
# Uncomment to run Gunicorn in the background.
# daemon = True

# Reload:
# Auto-reload on code changes. Useful in development, not recommended in production.
# reload = True
