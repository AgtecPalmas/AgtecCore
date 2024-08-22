# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim

EXPOSE 8000
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1
ENV APP_HOME /app/{{cookiecutter.project_slug.lower()}}

RUN mkdir -p $APP_HOME

# Setup project folder
WORKDIR $APP_HOME

# Install project libs
RUN apt-get clean && apt-get update \
    && apt-get -y install \
    ffmpeg \
    gcc \
    git \
    libc-dev \
    libffi-dev \
    libsm6 \
    libpq-dev \
    libxext6 \
    libxml2-dev \
    libxslt-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install pip requirements
COPY requirements.txt requirements-dev.txt ./

RUN pip install -U setuptools pip \
    && pip install -r requirements.txt \
    && pip install -r requirements-dev.txt

RUN mkdir -p $APP_HOME/static \
    && mkdir -p $APP_HOME/media \
# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
    && adduser -u 5678 --disabled-password --gecos "" appuser \
    && chown -R appuser $APP_HOME
USER appuser