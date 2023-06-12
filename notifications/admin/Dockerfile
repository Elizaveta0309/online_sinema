FROM python:3.10
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY ./requirements.txt .

# hadolint ignore=DL3013
RUN  pip install --upgrade pip \
     && pip install -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]