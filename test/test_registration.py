import allure

from api.client import register
from data.test_data import MSG_EMAIL_ALREADY_USED
from helpers.email_generator import generate_random_user


class TestRegistration:
    @allure.title("Успешная регистрация нового пользователя")
    def test_register_new_user_success(self, session):
        user = generate_random_user()
        resp = register(
            session,
            user["email"],
            user["password"],
            user["name"],
        )
        assert resp.status_code == 201
        assert resp.json()['user']['email'] == user['email']

    @allure.title("Ошибка при регистрации с дублирующимся email")
    def test_register_duplicate_email_returns_error(self, session, registered_user):
        resp = register(
            session,
            registered_user["email"],
            registered_user["password"],
            registered_user["name"],
        )
        assert resp.status_code == 400
        assert resp.json().get("message") == MSG_EMAIL_ALREADY_USED
