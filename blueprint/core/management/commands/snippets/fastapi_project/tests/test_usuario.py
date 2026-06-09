"""
===================================================================================================
Atenção:
===================================================================================================

Arquivo gerado pelo Build FastAPI.

Esse arquivo de testes deve ser utilizado como modelo para implementação
dos testes unitários e de integração da camada FastAPI.
"""

import pytest


@pytest.mark.asyncio
async def test_healthcheck(async_client):
    response = await async_client.get("/core/")
    _json = response.json()

    assert response.status_code == 200
    assert _json.get('status') == "ok"


@pytest.mark.asyncio
async def test_fetch_all(async_client):
    response = await async_client.get("/usuario/usuario/")
    assert response.status_code == 200
    assert response.json()["count"] == 0


@pytest.mark.asyncio
async def test_create_usuario(async_client):
    data = {
        "email": "email@email.com.br",
        "nome": "Nome do Usuário",
        "whatsapp": "123456789",
    }
    response = await async_client.post("/usuario/usuario/", json=data)
    assert response.status_code == 200
    assert response.json()["email"] == data["email"]

