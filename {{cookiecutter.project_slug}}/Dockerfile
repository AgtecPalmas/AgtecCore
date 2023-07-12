# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.9-slim

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

#variaveis gerais
ENV SECRET_KEY=''
ENV DEBUG=True
ENV ALLOWED_HOSTS=.localhost,
ENV API_PATH=http://localhost:8080/api/

#variaveis database
ENV DB_ENGINE=django.db.backends.sqlite3
ENV DB_NAME=dev.sqlite3
ENV DB_USER=usuario_do_banco_de_dados
ENV DB_PASSWORD=senha_do_banco_de_dados
ENV DB_HOST=endereco_do_servidor_do_banco_de_dados
ENV DB_PORT=5432

# Install pip requirements
COPY requirements.txt .
RUN apt-get update && \
    apt-get -y install sudo
RUN python -m pip install --upgrade pip && \
    python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

RUN python manage.py makemigrations
RUN python manage.py migrate

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser
