from api.client import login, extract_token


class TestAuthorization:
    def test_login_success(self, session, registered_user):
        resp = login(
            session,
            registered_user["email"],
            registered_user["password"],
        )
        assert resp.status_code == 201
        assert extract_token(resp.json())
