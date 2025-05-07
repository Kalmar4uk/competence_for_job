# Найти причину блокировки БД,
# вероятно pytest-django и fastapi.testclient
# мешают друг другу и блочат бд

import pytest
from competencies.fastapi_competencies import fastapi_competencies
from fastapi.testclient import TestClient
from django.contrib.auth.models import Group
from api.auth import create_token


@pytest.fixture
def client():
    return TestClient(fastapi_competencies)


@pytest.fixture
def authorized_user(django_user_model):
    user = django_user_model.objects.create_user(
        email="authorized@mail.ru",
        password="Authorized321"
    )
    return user


@pytest.fixture
def director_user(django_user_model):
    user = django_user_model.objects.create_user(
        email="director@mail.ru",
        password="Director321"
    )
    group = Group.objects.create(
        name="Директор"
    )
    user.groups.add(group)
    return user


@pytest.fixture
def auth_token_for_authorized_user(authorized_user):
    data = {"sub": authorized_user.email}
    return create_token(data)


@pytest.fixture
def auth_authorized_user(client, auth_token_for_authorized_user):
    client.headers.update({
        "Authorization": f"Bearer {auth_token_for_authorized_user}"
    })
    return client


@pytest.fixture
def auth_token_director(director_user):
    data = {"sub": director_user.email}
    return create_token(data)


@pytest.fixture
def auth_director(client, auth_token_director):
    client.headers.update({
        "Authorization": f"Bearer {auth_token_director}"
    })
    return client
