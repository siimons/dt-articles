# Указываем базовый образ Python
FROM python:3.12.3-alpine

# Устанавливаем зависимости для работы FastAPI и Uvicorn, а также сборки Python-зависимостей
RUN apk update && apk add --no-cache \
    mariadb-client \
    build-base \
    libffi-dev

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы приложения
COPY . .

# Открываем порт для приложения
EXPOSE 8000

# Запускаем FastAPI приложение с Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]