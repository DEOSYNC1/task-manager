# Официальный образ Python 3.12
FROM python:3.12-slim

# Не создавать байт-код и не писать буфер для логов в контейнере
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Рабочий каталог внутри контейнера
WORKDIR /app

# Копируем зависимости отдельно для кэширования слоя
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения
COPY src/ ./src/

# Каталог для данных и неизменяемый пользователь без прав root
RUN mkdir -p /app/data && useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Хранилище задач по умолчанию находится в томе /app/data
ENV TASKS_FILE=/app/data/tasks.json

# Точка входа: python -m src.main --file <TASKS_FILE>
ENTRYPOINT ["sh", "-c", "python -m src.main --file \"$TASKS_FILE\" \"$@\"", "--"]