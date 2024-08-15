FROM python:3.9.13-slim as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV CRYPTOGRAPHY_DONT_BUILD_RUST 1

WORKDIR /app

RUN apt-get clean && apt-get update
RUN apt-get -y install sudo gcc git libxml2-dev libxslt-dev libffi-dev libpq-dev libc-dev ffmpeg libsm6 libxext6
RUN apt-get clean && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

FROM python:3.9.13-slim

ENV HOME=/home/app
ENV APP_HOME=/home/app/{{cookiecutter.project_slug.lower()}}

RUN mkdir -p $APP_HOME

WORKDIR $APP_HOME

COPY --from=builder /usr/src/app/wheels /wheels
COPY . /app

# movendo dependencias instaladas na build para o projeto #
RUN mkdir -p $APP_HOME/static
RUN mkdir -p $APP_HOME/media

RUN pip install -U setuptools pip
RUN pip install --no-cache /wheels/*

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser $APP_HOME 
USER appuser
