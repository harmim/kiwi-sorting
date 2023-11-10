# Author: Dominik Harmim <harmim6@gmail.com>

FROM python:3.12-alpine

LABEL maintainer "Dominik Harmim <harmim6@gmail.com>"

RUN apk update && apk add bash make
RUN pip install --no-cache-dir pipenv

WORKDIR /usr/src/app
COPY Pipfile Pipfile.lock ./

RUN pipenv install --system --deploy

EXPOSE 5000
