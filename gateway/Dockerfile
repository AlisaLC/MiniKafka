FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install wget -y
RUN wget https://github.com/prometheus/node_exporter/releases/download/v1.3.1/node_exporter-1.3.1.linux-amd64.tar.gz
RUN tar xvf node_exporter-1.3.1.linux-amd64.tar.gz
RUN cd node_exporter-1.3.1.linux-amd64
RUN bash -c "/app/node_exporter-1.3.1.linux-amd64/node_exporter &"

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

ARG HOST
ENV HOST ${HOST}
ARG PORT
ENV PORT ${PORT}

CMD gunicorn --worker-class=gevent --worker-connections=1000 --workers=5 -b ${HOST}:${PORT} gateway:app