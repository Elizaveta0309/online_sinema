#!/usr/bin/env bash

./wait-for-it.sh postgres:5432 -t 15
./wait-for-it.sh redis:6379 -t 15
./wait-for-it.sh elasticsearch:9200 -t 30
python load_data.py
