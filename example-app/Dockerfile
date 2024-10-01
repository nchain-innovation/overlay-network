FROM python:3.12-slim-bookworm AS base

ENV PYTHONUNBUFFERED=1
ENV TZ=Europe/London
ENV DEBIAN_FRONTEND="noninteractive"

WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

FROM base AS release
WORKDIR /app/python

# env var to detect we are in a docker instance
ENV APP_ENV=docker
EXPOSE 3050
CMD [ "python3", "main.py"]