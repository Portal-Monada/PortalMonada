FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip --progress-bar off

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt --progress-bar off

COPY . /app/
