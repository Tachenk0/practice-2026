#default
DEFAULT_ROWS =9
DEFAULT_COLS =9
DEFAULT_MINES =10
#limits
MIN_ROWS =5
MAX_ROWS =30
MIN_COLS =5
MAX_COLS =30
MIN_MINES =1

#Difficult
PRESETS = {
    "Новичок:": {"rows": 8,"cols": 8,"mines": 9},
    "Любитель:": {"rows": 9, "cols": 9, "mines": 10},
    "Профессионал:": {"rows": 16, "cols": 16, "mines": 40},
    "Эксперт:": {"rows": 30, "cols": 16, "mines": 99}
}
#records
RECORDS_FILE = "data/records.json"
MAX_RECORDS = 10

#UI
CELL_SIZE_MIN = 20
CELL_SIZE_MAX = 40
WINDOW_MAX_WIDTH = 800
WINDOW_MAX_HEIGHT = 600