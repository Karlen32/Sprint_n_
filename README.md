# API-тесты «Доска объявлений»

Автотесты для учебного сервиса [Доска](https://qa-desk.stand.praktikum-services.ru/)

## Установка

```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Запуск тестов

```bash
pytest -v
```

## Структура

- `data/test_data.py` — URL, константы, категории
- `helpers/email_generator.py` — генерация уникального email
- `api/client.py` — запросы к API
- `test/` — тесты по функциональностям
- `conftest.py` — фикстуры
# Sprint_n_
# Sprint_n_
# Sprint_n_
