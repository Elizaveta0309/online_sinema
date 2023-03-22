FROM python:3.10.7-slim

WORKDIR /opt/tests

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt
COPY wait-for-it.sh wait-for-it.sh
COPY run.sh run.sh
RUN chmod +x wait-for-it.sh
RUN chmod +x run.sh

RUN pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir

COPY . .

ENTRYPOINT ["./run.sh"]
