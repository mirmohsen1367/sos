import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture(scope="session")
def client():
    return APIClient()


@pytest.fixture
def user(db):
    user = User.objects.create_user(
        password="admin", username="admin", email="admin@gmail.com"
    )
    return user
