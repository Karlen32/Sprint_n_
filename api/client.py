import allure
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

from data.test_data import (
    BASE_URL,
    API_REGISTER,
    API_LOGIN,
    API_ADS,
    API_UPDATE_OFFER,
    API_LISTINGS,
    API_DELETE_USER,
    AD_TITLE,
    AD_DESCRIPTION,
    AD_CONDITION,
    AD_CITY,
    AD_PRICE,
)


@allure.step("Создание payload объявления")
def _create_listing_payload(title, description, category, condition, city, price=None):
    return {
        "name": title,
        "description": description,
        "category": category,
        "condition": condition or AD_CONDITION,
        "city": city or AD_CITY,
        "price": price if price is not None else AD_PRICE,
    }


@allure.step("Извлечение токена из ответа")
def extract_token(data):
    if not data:
        return None
    tok = data.get("token") or data.get("access_token")
    if isinstance(tok, dict):
        return tok.get("access_token") or tok.get("token")
    return tok


@allure.step("Парсинг ответа с объявлением")
def parse_listing_response(resp):
    data = resp.json() or {}
    listing = data.get("listing") or data
    return {
        "id": listing.get("id"),
        "title": listing.get("name") or listing.get("title"),
        "description": listing.get("description"),
    }


@allure.step("Получение HTTP-сессии")
def get_session():
    session = requests.Session()
    session.verify = False
    session.headers["Content-Type"] = "application/json"
    return session


@allure.step("Регистрация пользователя")
def register(session, email, password, name):
    url = BASE_URL + API_REGISTER
    payload = {"email": email, "password": password, "name": name}
    return session.post(url, json=payload, timeout=15)


@allure.step("Вход в систему")
def login(session, email, password):
    url = BASE_URL + API_LOGIN
    payload = {"email": email, "password": password}
    return session.post(url, json=payload, timeout=15)


@allure.step("Создание объявления")
def create_ad(session, token, title, description, category, condition=None, city=None, price=None):
    url = BASE_URL + API_ADS
    condition = condition or AD_CONDITION
    city = city or AD_CITY
    payload = _create_listing_payload(title, description, category, condition, city, price)
    payload_str = {k: str(v) for k, v in payload.items()}
    m = MultipartEncoder(fields=payload_str)
    headers = {"Authorization": f"Bearer {token}", "Content-Type": m.content_type}

    return session.post(url, data=m, headers=headers, timeout=180)


@allure.step("Обновление объявления")
def update_ad(session, token, ad_id, title=None, description=None, category=None, condition=None, city=None, price=None):
    url = BASE_URL + API_UPDATE_OFFER + f"/{ad_id}"
    headers = {"Authorization": f"Bearer {token}"}
    payload = _create_listing_payload(
        title or AD_TITLE,
        description or AD_DESCRIPTION,
        category or "Авто",
        condition,
        city,
        price,
    )
    return session.patch(url, json=payload, headers=headers, timeout=30)


@allure.step("Удаление объявления")
def delete_ad(session, token, ad_id):
    url = BASE_URL + API_LISTINGS + f"/{ad_id}"
    headers = {"Authorization": f"Bearer {token}"}
    return session.delete(url, headers=headers, timeout=30)


@allure.step("Удаление пользователя")
def delete_user(session, token):
    url = BASE_URL + API_DELETE_USER
    headers = {"Authorization": f"Bearer {token}"}
    return session.delete(url, headers=headers, timeout=15)
