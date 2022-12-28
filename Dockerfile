FROM python:3.10.9-alpine
 
ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /base
COPY ./base /base
WORKDIR /base