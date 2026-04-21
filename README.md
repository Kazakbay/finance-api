# Finance API

Простой API для учета доходов и расходов.

## Запуск

pip install -r requirements.txt
uvicorn main:app --reload

## Эндпоинты

- GET / — проверка что работает
- POST /add — добавить транзакцию
- GET /list — список транзакций