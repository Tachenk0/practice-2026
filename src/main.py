import sys
import argparse
import json
from src.ui import MinesweeperUI
from src.config import DEFAULT_ROWS, DEFAULT_COLS, DEFAULT_MINES


def parse_args():
    parser = argparse.ArgumentParser(
        description='Сапёр - классическая игра с BFS и дедукцией',
        epilog='Пример: python src/main.py --input data/sample_input.json'
    )

    parser.add_argument(
        '--input',
        type=str,
        default='data/sample_input.json',
        help='Путь к файлу с входными данными (по умолчанию: data/sample_input.json)'
    )

    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Путь к файлу результата (по умолчанию: stdout)'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Подробный вывод'
    )

    parser.add_argument(
        '--headless',
        action='store_true',
        help='Запуск без GUI (для тестирования)'
    )

    parser.add_argument(
        '--rows',
        type=int,
        default=DEFAULT_ROWS,
        help=f'Количество строк (по умолчанию: {DEFAULT_ROWS})'
    )

    parser.add_argument(
        '--cols',
        type=int,
        default=DEFAULT_COLS,
        help=f'Количество столбцов (по умолчанию: {DEFAULT_COLS})'
    )

    parser.add_argument(
        '--mines',
        type=int,
        default=DEFAULT_MINES,
        help=f'Количество мин (по умолчанию: {DEFAULT_MINES})'
    )

    return parser.parse_args()


def load_input_data(input_file: str):

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        print(f" Ошибка парсинга JSON: {e}")
        sys.exit(1)


def main():

    args = parse_args()

    if args.verbose:
        print("Сапёр")
        print(f"Входной файл: {args.input}")
        print(f"Размер поля: {args.rows}×{args.cols}")
        print(f"💣 Количество мин: {args.mines}")

    # load input data
    input_data = load_input_data(args.input)
    if input_data and args.verbose:
        print(f"Загружены данные: {json.dumps(input_data, indent=2)}")

    # Запуск в headless режиме
    if args.headless:
        print(" Запуск в headless режиме")
        return

    # Запуск GUI
    try:
        app = MinesweeperUI()
        app.run()
    except Exception as e:
        print(f" Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
