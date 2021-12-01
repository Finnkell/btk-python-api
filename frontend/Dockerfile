# syntax=docker/dockerfile:1
FROM python:3.8.12

EXPOSE 8501

WORKDIR /usr/

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .