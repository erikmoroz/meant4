# Better to use the image with sha256 hash to be able to reproduce bugs and errors
FROM python:3.10.13-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /src
COPY ./ /src
WORKDIR /src/api

RUN apt update && apt install -y --no-install-recommends postgresql-client python3-pip build-essential python3-dev python-setuptools libcurl4-openssl-dev libffi-dev libssl-dev libpq-dev git gettext
RUN apt install -y build-essential libpq-dev zlib1g-dev xvfb
RUN pip install -r requirements.txt

RUN chmod +x /src/entrypoint.sh

EXPOSE 8282