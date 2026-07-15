# Сапёр — учебная ознакомительная практика 2026

**Студент:** Иванов Иван Иванович  
**Группа:** БИ-01-01  
**Вариант:** Б-26 — Сапёр (волновой алгоритм BFS + дедукция)  
**Язык:** Python 3.12

---

## Описание

Классическая игра «Сапёр» с реализацией волнового алгоритма (BFS) для открытия пустых ячеек и алгоритма дедукции для генерации подсказок. Поддерживаются четыре уровня сложности с предустановленными размерами полей: 8×8 (9 мин), 9×9 (10 мин), 16×16 (40 мин) и 30×16 (99 мин). Реализован графический интерфейс на Tkinter, таймер и таблица рекордов с сохранением в JSON-файл.

---

## Структура репозитория
```
.
├── src/
│ ├── main.py # точка входа, CLI
│ ├── game.py # основная логика игры
│ ├── board.py # игровое поле
│ ├── cell.py # класс ячейки
│ ├── algorithm.py # алгоритмическое ядро (BFS, дедукция)
│ ├── ui.py # графический интерфейс
│ ├── timer.py # таймер
│ ├── records.py # работа с рекордами
│ └── config.py # конфигурация и настройки
├── tests/
│ ├── test_algorithm.py # юнит-тесты алгоритмов
│ ├── test_board.py # юнит-тесты игрового поля
│ ├── test_cell.py # юнит-тесты ячейки
│ ├── test_game.py # юнит-тесты игровой логики
│ ├── test_records.py # юнит-тесты рекордов
│ └── test_integration.py # интеграционные тесты
├── data/
│ ├── sample_input.json # пример входных данных
│ ├── expected_output.json # ожидаемый результат для тестов
│ └── records.json # файл с рекордами
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
├── requirements.txt
└── README.md
```
---

## Установка и запуск

### Локально
```
# 1. Клонировать репозиторий
git clone https://github.com/Tachenk0/minesweeper.git
cd minesweeper

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Запустить игру
python -m src.main
```
## В Docker
```
# Собрать образ
docker build -t minesweeper .

# Запустить игру
docker run --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix minesweeper

# Запустить с внешним файлом данных
docker run --rm -v "$(pwd)/data:/app/data" minesweeper --input /app/data/sample_input.json
```


## Параметры запуска

| Параметр | Описание | По умолчанию |
|:---------|:---------|:------------:|
| `--input` | Путь к файлу с входными данными | `data/sample_input.json` |
| `--output` | Путь к файлу результата | `stdout` |
| `--verbose` | Подробный вывод | `выключен` |
| `--headless` | Запуск без GUI (для тестирования) | `выключен` |
| `--rows` | Количество строк | `9` |
| `--cols` | Количество столбцов | `9` |
| `--mines` | Количество мин | `10` |

Запуск тестов
```
# Запуск всех тестов
python -m pytest tests/ -v

# Запуск с покрытием кода
python -m pytest tests/ --cov=src --cov-report=html

# Запуск в Docker
docker run --rm --entrypoint python minesweeper -m pytest tests/ -v
```
Зависимости
Python ≥ 3.12

Tkinter

pytest ≥ 7.0.0
