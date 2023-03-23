FROM python:3.10.7-slim

WORKDIR /opt/etl

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y netcat

COPY etl/requirements.txt requirements.txt
COPY etl/wait-for-it.sh wait-for-it.sh
COPY etl/run_etl.sh run_etl.sh
RUN chmod +x wait-for-it.sh
RUN chmod +x run_etl.sh

RUN pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir

COPY etl .

ENTRYPOINT ["./run_etl.sh"]