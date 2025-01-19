import pytest
from django.urls import reverse
from django.test.client import Client


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create(
        email="user@mail.ru",
        personnel_number="11111111"
    )


@pytest.fixture
def user_client(user):
    client = Client()
    client.force_login(user)
    return client


@pytest.fixture
def url_home():
    return reverse("matrix:main")


@pytest.fixture
def url_matrix():
    return reverse("matrix:matrix")


@pytest.fixture
def url_login():
    return reverse("users:login")


@pytest.fixture
def url_logout():
    return reverse("users:logout")


@pytest.fixture
def url_profile(user):
    return reverse("matrix:profile", args=[user.personnel_number])
