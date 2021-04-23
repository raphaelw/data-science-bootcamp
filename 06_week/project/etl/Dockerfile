# syntax=docker/dockerfile:1
FROM python:3.9.4-slim

WORKDIR /app
COPY ./app .
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt
CMD ["python", "etl.py"]