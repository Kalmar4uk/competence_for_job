import pytest


def test_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"hello": "Здарова, чекни доку /api/docs или /api/redoc"}


def test_get_all_companies(auth_authorized_user):
    response = auth_authorized_user.get("/companies")
    assert response.status_code == 200
