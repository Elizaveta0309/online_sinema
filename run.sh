#!/usr/bin/env bash

./wait-for-it.sh redis:6379 -t 15
./wait-for-it.sh elasticsearch:9200 -t 30
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
