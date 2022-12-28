FROM python:3.10.9-alpine
 
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add python3-dev gcc libc-dev

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . .