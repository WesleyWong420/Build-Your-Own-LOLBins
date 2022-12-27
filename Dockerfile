FROM python:3.7-alpine
 
ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /requirements.txt