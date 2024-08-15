# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim

EXPOSE 8000
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Setup project folder
WORKDIR /app/{{cookiecutter.project_slug.lower()}}

# Install project libs
RUN apt-get clean && apt-get update
RUN apt-get -y install sudo gcc git libxml2-dev libxslt-dev libffi-dev libpq-dev libc-dev ffmpeg libsm6 libxext6
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Install pip requirements
COPY requirements.txt .
COPY requirements-dev.txt .
RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt