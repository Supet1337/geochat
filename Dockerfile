FROM python:3.7

ENV PYTHONUNBUFFERED 1
RUN mkdir /web
WORKDIR /web
COPY requirements.txt /web/
RUN pip3 install -r requirements.txt

RUN apt-get update && \
    apt-get install -y build-essential libzbar-dev

COPY . /web/

