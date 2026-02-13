from api.client import delete_ad


class TestDeleteAd:
    def test_delete_ad_by_owner_success(self, session, auth_token, created_ad_id):
        resp = delete_ad(session, auth_token, created_ad_id)
        assert resp.status_code == 200
