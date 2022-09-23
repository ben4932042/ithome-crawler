FROM python:3.7-slim
LABEL org.opencontainers.image.source https://github.com/ben4932042/ithome-crawler
LABEL org.opencontainers.image.title="2022 ithome demo crawler"
LABEL org.opencontainers.image.description="just for research, please don't use in production."
ENV TZ="Asia/Taipei"
RUN mkdir /crawler
WORKDIR /crawler
COPY . /crawler
RUN pip install --no-cache-dir -r requirements.txt
