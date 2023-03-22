#!/usr/bin/env bash

./wait-for-it.sh postgres-test:5432 -t 15
./wait-for-it.sh redis-test:6379 -t 15
./wait-for-it.sh elasticsearch-test:9200 -t 30
gunicorn src.main:app --bind 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker