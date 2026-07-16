FROM python:3.12-slim

# Установка системных зависимостей для Tkinter
RUN apt-get update && apt-get install -y \
    tk \
    x11-apps \
    xauth \
    && rm -rf /var/lib/apt/lists/*

# Рабочая папка
WORKDIR /app

# Копирование зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование всего кода
COPY . .

# Создание папки для данных и файла рекордов
RUN mkdir -p /app/data && \
    echo "[]" > /app/data/records.json && \
    chmod -R 777 /app/data

# Создание файла sample_input.json
RUN echo '{"rows": 9, "cols": 9, "mines": 10, "level": "Любитель"}' > /app/data/sample_input.json

# Настройка X11 для автоматического подключения
ENV DISPLAY=:0
ENV QT_X11_NO_MITSHM=1

# Создаем скрипт-обертку для запуска
RUN echo '#!/bin/bash\n\
# Проверка и настройка X11\n\
if [ -z "$DISPLAY" ]; then\n\
    export DISPLAY=:0\n\
fi\n\
\n\
# Проверка доступа к X11\n\
if command -v xhost &> /dev/null; then\n\
    xhost +local:docker 2>/dev/null || true\n\
fi\n\
\n\
# Запуск игры\n\
python -m src.main "$@"' > /entrypoint.sh && chmod +x /entrypoint.sh

# Точка входа
ENTRYPOINT ["/entrypoint.sh"]
CMD []
