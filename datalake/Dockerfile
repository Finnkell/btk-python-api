# syntax=docker/dockerfile:1
FROM python:3.8.12
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN pip install plyvel
COPY . /code/