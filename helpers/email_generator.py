from faker import Faker

from data.test_data import DEFAULT_NAME, DEFAULT_PASSWORD

_faker = Faker()


def generate_random_user():
    fn = _faker.first_name()[:14].strip()
    ln = _faker.last_name()[:15].strip()
    name = (fn + " " + ln).strip()[:30] or DEFAULT_NAME
    return {
        "email": _faker.unique.email(),
        "name": name,
        "password": DEFAULT_PASSWORD,
    }
