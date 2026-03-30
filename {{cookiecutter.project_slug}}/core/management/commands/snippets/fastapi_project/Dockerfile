# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.9-slim

EXPOSE 8181

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Create PostgreSQL user and database
# TODO trocar o nome do sistema
ENV POSTGRES_USER=TROCAR_PELO_NOME_DO_SISTEMA_dbmanager_2LiyBoLHeHo5yG
ENV POSTGRES_PASSWORD=senha_padrao_deve_ser_mudada

# Define o diretório de trabalho
WORKDIR /app

COPY pyproject.toml uv.lock ./

# instala uv
RUN pip install uv

# instala dependências
RUN uv sync --frozen

COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

