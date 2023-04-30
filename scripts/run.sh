#!/bin/bash 
set -e
set -x

gunicorn -b 0.0.0.0:8000 -w 4 -k uvicorn.workers.UvicornWorker main:app