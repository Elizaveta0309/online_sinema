FROM python:3.10

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

COPY requirements.txt requirements.txt
COPY tests/api/.env .env
COPY tests/api/run.sh run.sh
COPY wait-for-it.sh wait-for-it.sh
RUN chmod +x wait-for-it.sh
RUN chmod +x run.sh

RUN  pip install --upgrade pip && pip install -r requirements.txt


ENTRYPOINT ["./run.sh"]
