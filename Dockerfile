# Базовый образ — официальный Python 3.11
FROM python:3.11-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# Сначала копируем только requirements.txt — для кеширования слоёв.
# Если код поменялся, а зависимости нет — pip install не будет перезапускаться.
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем весь остальной код проекта
COPY . .

# Открываем порт, на котором будет работать API
EXPOSE 8000

# Команда запуска — uvicorn запустит твой FastAPI app
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]