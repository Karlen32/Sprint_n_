import allure

from api.client import create_ad, parse_listing_response
from data.test_data import AD_TITLE, AD_DESCRIPTION, CATEGORIES


class TestCreateAd:
    @allure.title("Успешное создание объявления")
    def test_create_ad_success(self, session, auth_token):
        resp = create_ad(
            session, auth_token, AD_TITLE, AD_DESCRIPTION, CATEGORIES[0]
        )
        assert resp.status_code == 201
        data = parse_listing_response(resp)
        assert data["id"]
        assert data["title"] == AD_TITLE
        assert data["description"] == AD_DESCRIPTION
