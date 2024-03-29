FROM python:3.11-alpine

ENV PYTHONUNBUFFERED=1

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . ./megano

WORKDIR /megano

LABEL authors="maksim"

