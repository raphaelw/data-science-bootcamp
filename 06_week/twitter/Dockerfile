# syntax=docker/dockerfile:1

FROM python:3.9.4-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt
COPY ./app .
CMD ["python", "get_tweets_streaming.py"]