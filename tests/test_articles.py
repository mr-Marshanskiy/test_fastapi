from fastapi import status
from fastapi.testclient import TestClient

from app.const import (
    ARTICLES_URL,
)
from app.main import app


client = TestClient(app)


def test_get_article(headers):
    params = {}

    response = client.get("/" + ARTICLES_URL + f'/{2}', headers=headers, params=params)
    schema = response.json()
    print(schema)

    assert response.status_code == status.HTTP_200_OK
    assert schema["id"] == 2


def test_get_articles(headers):
    params = {}

    url = "/" + ARTICLES_URL
    response = client.get(url, headers=headers, params=params)
    schema = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(schema) > 0
