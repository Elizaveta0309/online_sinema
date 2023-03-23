#!/usr/bin/env bash

./wait-for-it.sh postgres-test:5432 -t 15
./wait-for-it.sh redis-test:6379 -t 15
./wait-for-it.sh elasticsearch-test:9200 -t 30
python load_data.py
