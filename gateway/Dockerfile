FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

ARG HOST
ENV HOST ${HOST}
ARG PORT
ENV PORT ${PORT}

CMD flask --app gateway run --host ${HOST} --port ${PORT}