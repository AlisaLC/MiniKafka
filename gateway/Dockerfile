FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

ARG HOST
ENV HOST ${HOST}
ARG PORT
ENV PORT ${PORT}

CMD gunicorn --worker-class=gevent --worker-connections=1000 --workers=5 -b ${HOST}:${PORT} gateway:app