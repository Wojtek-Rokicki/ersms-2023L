# Config file
wsgi_app = 'ersms_test.api.app:app'

# Server socket
bind = ['0.0.0.0:8080']

# Worker Options
workers = 8
worker_class = 'uvicorn.workers.UvicornWorker'

# Logging
loglevel = 'info'
