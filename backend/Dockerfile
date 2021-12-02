# syntax=docker/dockerfile:1
FROM python:3.9-slim
LABEL maintainer="btk.com.br"

ENV PYTHONUNBUFFERED=1

WORKDIR /code_branch

COPY requirements.txt .

RUN apt-get update && \
    apt-get -y install libpq-dev gcc python3-dev musl-dev && \
    apt-get -y install libffi-dev && \
    /usr/local/bin/python -m pip install --upgrade pip && \
    pip install psycopg2 && \
    pip install -r requirements.txt

COPY . /code_branch/