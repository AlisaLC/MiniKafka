FROM python:3.10-slim

WORKDIR /app

RUN wget https://github.com/prometheus/node_exporter/releases/download/v1.3.1/node_exporter-1.3.1.linux-amd64.tar.gz
RUN tar xvf node_exporter-1.3.1.linux-amd64.tar.gz
RUN cd node_exporter-1.3.1.linux-amd64
RUN ./node-exporter

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "zookeeper.py"]