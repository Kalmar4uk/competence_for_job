from http import HTTPStatus

import pytest


@pytest.mark.parametrize(
    "name", (
        pytest.lazy_fixture("url_login"),
    )
)
def test_pages_for_anonymous_user(client, name):
    response = client.get(name)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    "name", (
        (pytest.lazy_fixture("url_login")),
        (pytest.lazy_fixture("url_matrix")),
        (pytest.lazy_fixture("url_profile")),
        (pytest.lazy_fixture("url_home"))
    )
)
@pytest.mark.parametrize(
    "parametrized_client, expected_status", (
        (pytest.lazy_fixture("user_client"), HTTPStatus.OK),
    )
)
def test_pages_availability_for_user(
    name, parametrized_client, expected_status
):
    response = parametrized_client.get(name)
    assert response.status_code == expected_status
