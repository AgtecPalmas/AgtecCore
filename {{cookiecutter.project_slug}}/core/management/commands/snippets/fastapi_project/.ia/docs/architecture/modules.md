# Estrutura Modular

Cada módulo funcional segue o padrão:

- models.py → Modelos SQLAlchemy
- schemas.py → Schemas Pydantic
- routers.py → Endpoints FastAPI
- use_cases.py → Lógica de negócio

## Regras

- Um módulo não acessa diretamente outro
- Comunicação entre módulos ocorre via contratos explícitos

## Regra de Configuração por Módulo

- Configuração transversal da API permanece em `core.config.Settings`.
- Quando um módulo tiver integração externa específica (ex.: IA generativa), deve manter settings próprios para evitar acoplamento indevido — nunca usar `core.config.Settings` como fonte de configuração de IA ou de integrações externas isoladas.
