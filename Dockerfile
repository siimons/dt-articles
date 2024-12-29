# Указываем базовый образ Python на основе slim-версии Ubuntu
FROM python:3.12-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    mariadb-client \
    gcc \
    libffi-dev \
    build-essential \
    libssl-dev \
    default-libmysqlclient-dev \
    wget \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Копируем wait-for-it.sh для проверки доступности MySQL
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем Python-зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем оставшиеся файлы приложения
COPY . .

# Открываем порт для приложения
EXPOSE 8000

# Запускаем приложение FastAPI через Uvicorn, проверяя доступность MySQL
CMD ["/wait-for-it.sh", "mysql:3306", "--", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]