FROM python:3.12-slim

# Установка системных зависимостей для Tkinter и X11
RUN apt-get update && apt-get install -y \
    tk \
    x11-apps \
    xauth \
    && rm -rf /var/lib/apt/lists/*

# Рабочая папка внутри контейнера
WORKDIR /app

# Копирование файла с зависимостями
COPY requirements.txt .

# Установка Python-зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование всего кода проекта
COPY . .

# Создание папки для данных с правильными правами
RUN mkdir -p /app/data && chmod 777 /app/data

# Устанавливаем переменную для X11 (по умолчанию)
ENV DISPLAY=:0

# Команда по умолчанию при запуске контейнера
CMD ["python", "-m", "src.main"]
