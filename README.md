# Finance API

REST API для учета личных финансов. Позволяет добавлять транзакции и просматривать историю.

## Технологии

- Python 3
- FastAPI
- SQLAlchemy
- SQLite

## Запуск

git clone https://github.com/Kazakbay/finance-api.git
cd finance-api
pip install -r requirements.txt
uvicorn main:app --reload

Открой http://localhost:8000/docs

## Эндпоинты

- GET / — проверка что работает
- POST /add?amount=5000&category=еда — добавить транзакцию
- GET /list — список всех транзакций