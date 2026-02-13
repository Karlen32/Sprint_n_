from api.client import update_ad, parse_listing_response
from data.test_data import AD_TITLE_EDITED, AD_DESCRIPTION, CATEGORIES


class TestEditAd:
    def test_edit_ad_by_owner_success(self, session, auth_token, created_ad_id):
        resp = update_ad(
            session, auth_token, created_ad_id,
            title=AD_TITLE_EDITED,
            description=AD_DESCRIPTION,
            category=CATEGORIES[0],
        )
        assert resp.status_code == 200
        data = parse_listing_response(resp)
        assert data["title"] == AD_TITLE_EDITED

    def test_edit_ad_by_another_user_forbidden(
        self, session, created_ad_id, another_user_token
    ):
        resp = update_ad(
            session, another_user_token, created_ad_id,
            title=AD_TITLE_EDITED,
            description=AD_DESCRIPTION,
            category=CATEGORIES[0],
        )
        assert resp.status_code == 401
        assert resp.json().get("message") == "Оффер не найден или у вас нет прав на его редактирование"
