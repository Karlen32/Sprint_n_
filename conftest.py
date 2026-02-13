import pytest

from api.client import get_session, register, login, create_ad, delete_user, extract_token
from data.test_data import (
    AD_TITLE,
    AD_DESCRIPTION,
    CATEGORIES,
)
from helpers.email_generator import generate_random_user


@pytest.fixture
def session():
    return get_session()


@pytest.fixture
def registered_user(session):
    user = generate_random_user()
    register(
        session,
        user["email"],
        user["password"],
        user["name"],
    )
    yield user
    login_resp = login(session, user["email"], user["password"])
    if login_resp.status_code in (200, 201):
        data = login_resp.json()
        token = extract_token(data)
        if token:
            delete_user(session, token)


@pytest.fixture
def auth_token(session, registered_user):
    resp = login(
        session,
        registered_user["email"],
        registered_user["password"],
    )
    token = extract_token(resp.json())
    return token


@pytest.fixture
def created_ad_id(session, auth_token):
    category = CATEGORIES[0]
    resp = create_ad(
        session, auth_token, AD_TITLE, AD_DESCRIPTION, category
    )
    ad_id = resp.json().get("id")
    return ad_id


@pytest.fixture
def another_user_token(session):
    user = generate_random_user()
    register(session, user["email"], user["password"], user["name"])
    login_resp = login(session, user["email"], user["password"])
    token = extract_token(login_resp.json())
    yield token
    delete_user(session, token)
