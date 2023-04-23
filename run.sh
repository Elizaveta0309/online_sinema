#!/usr/bin/env bash

./wait-for-it.sh postgres:5432 -t 15
./wait-for-it.sh redis:6379 -t 15
./wait-for-it.sh elasticsearch:9200 -t 30
#gunicorn src.main:app --bind 0.0.0.0:8000 --reload -k uvicorn.workers.UvicornWorker
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
