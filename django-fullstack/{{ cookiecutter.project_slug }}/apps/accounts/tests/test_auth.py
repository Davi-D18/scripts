import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse


def test_login_page_renders(client):
    assert client.get(reverse("login")).status_code == 200


def test_register_page_renders(client):
    assert client.get(reverse("register")).status_code == 200


@pytest.mark.django_db
def test_register_creates_user(client):
    response = client.post(
        reverse("register"),
        {
            "username": "alice",
            "email": "alice@example.com",
            "password1": "SuperSecret123",
            "password2": "SuperSecret123",
        },
    )
    assert response.status_code == 302
    assert get_user_model().objects.filter(username="alice").exists()
