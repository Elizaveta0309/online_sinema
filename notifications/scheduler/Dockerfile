FROM python:3.10

WORKDIR /scheduler

COPY ./requirements.txt .


# hadolint ignore=DL3013
RUN  pip install --upgrade pip \
     && pip install -r requirements.txt --no-cache-dir

CMD ["python", "src/main.py"]