FROM python:3.7-slim
LABEL org.opencontainers.image.source https://github.com/ben4932042/ithome-crawler
RUN mkdir /crawler
WORKDIR /crawler
COPY . /crawler
RUN pip install --no-cache-dir -r requirements.txt
