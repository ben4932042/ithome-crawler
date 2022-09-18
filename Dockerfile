FROM python:3.7-slim

RUN mkdir /crawler
WORKDIR /crawler
COPY . /crawler
RUN pip install --no-cache-dir -r requirements.txt
