from multiprocessing import cpu_count

# Socket Path
bind = "unix:/root/projects/python/demo-api/gunicorn.sock"


# Worker Options
workers = cpu_count() + 1
worker_class = "uvicorn.workers.UvicornWorker"


# Logging Options
loglevel = "debug"
accesslog = "/root/projects/python/demo-api/access_log"
errorlog = "/root/projects/python/demo-api/error_log"
