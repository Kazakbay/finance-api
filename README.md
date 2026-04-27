# Finance API

[![CI](https://github.com/Kazakbay/finance-api/actions/workflows/ci.yml/badge.svg)](https://github.com/Kazakbay/finance-api/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136-009688.svg)](https://fastapi.tiangolo.com/)

REST API для учёта личных финансовых транзакций. Pet-проект, написанный для практики backend-разработки на Python.

## Стек

- **Python 3.11** + **FastAPI** — веб-фреймворк
- **SQLAlchemy** — ORM
- **SQLite** — база данных
- **Pytest** — юнит-тесты
- **Docker** + **Docker Compose** — контейнеризация
- **GitHub Actions** — CI: автозапуск тестов и линтера на каждый push
- **Ruff** — линтер и форматтер

## Возможности

- CRUD-операции для финансовых транзакций (сумма, категория)
- Автогенерируемая документация (Swagger UI / ReDoc)
- Покрытие юнит-тестами
- Конфигурация через переменные окружения
- Запуск одной командой через Docker Compose

## Запуск локально

### Через Python

```bash
# 1. Клонировать репозиторий
git clone https://github.com/Kazakbay/finance-api.git
cd finance-api

# 2. Создать виртуальное окружение
python -m venv .venv

# 3. Активировать (Windows)
.venv\Scripts\activate

# Активировать (Linux / macOS)
source .venv/bin/activate

# 4. Установить зависимости
pip install -r requirements.txt

# 5. Запустить сервер
uvicorn main:app --reload
```

API будет доступен на `http://localhost:8000`

### Через Docker Compose

```bash
docker-compose up --build
```

## Документация API

После запуска открой в браузере:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Тесты

```bash
pytest -v
```

## Конфигурация

Приложение читает настройки из переменных окружения. Для локального запуска значения по умолчанию подойдут — никаких настроек не требуется.

| Переменная     | Значение по умолчанию          | Описание                |
|----------------|--------------------------------|-------------------------|
| `DATABASE_URL` | `sqlite:///./finance.db`       | Строка подключения к БД |

Чтобы переопределить — скопируй `.env.example` в `.env` и поправь значения.

## Структура проекта

```
finance-api/
├── .github/workflows/    # GitHub Actions (CI)
├── main.py               # точка входа FastAPI, эндпоинты
├── database.py           # настройка SQLAlchemy и модели
├── test_main.py          # юнит-тесты
├── Dockerfile            # сборка контейнера с API
├── docker-compose.yaml   # оркестрация контейнеров
├── requirements.txt      # Python-зависимости
├── .env.example          # пример переменных окружения
├── .dockerignore
├── .gitignore
└── README.md
```

## CI

На каждый push в `main` GitHub Actions автоматически:

1. Проверяет код линтером (`ruff check`)
2. Проверяет форматирование (`ruff format --check`)
3. Запускает все тесты (`pytest`)
4. Собирает Docker-образ

Статус последнего запуска отображается в бейдже в верхней части README.

## Автор

Нурдаулет — студент Astana IT University, изучаю backend-разработку на Python.

- GitHub: [@Kazakbay](https://github.com/Kazakbay)