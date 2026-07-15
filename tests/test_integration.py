import unittest
import json
import tempfile
import os
from pathlib import Path
from src.game import Game
from src.records import RecordsManager


class TestIntegration(unittest.TestCase):
    # Интеграционные тесты

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.records_file = os.path.join(self.temp_dir, 'records.json')

        self.records_manager = RecordsManager()
        self.records_manager.records_file = self.records_file
        self.records_manager._ensure_file_exists()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_full_game_flow(self):
        # Тест полного игрового процесса
        game = Game(9, 9, 10)
        game.start()
        game.click(4, 4)

        self.assertFalse(game.board.first_click)
        self.assertFalse(game.is_game_over)
        self.assertFalse(game.is_won)

        revealed = sum(1 for cell in game.board.get_all_cells() if cell.is_revealed)
        self.assertGreater(revealed, 0)

    def test_bfs_and_game_integration(self):
        # Тест интеграции BFS с игрой
        game = Game(9, 9, 10)
        game.board.place_mines(4, 4)
        found = False

        for r in range(game.rows):
            for c in range(game.cols):
                cell = game.board.get_cell(r, c)
                if cell and not cell.is_mine and cell.adjacent_mines == 0:
                    game.click(r, c)
                    revealed = sum(1 for c in game.board.get_all_cells() if c.is_revealed)
                    self.assertGreater(revealed, 1)
                    found = True
                    break
            if found:
                break

        if not found:
            self.skipTest("Нет пустых клеток для теста")

    def test_deduction_and_game_integration(self):
        # Тест интеграции дедукции с игрой
        game = Game(9, 9, 10)
        game.board.place_mines(4, 4)

        hint = game.get_hint()
        if hint:
            row, col, is_mine = hint
            self.assertIsInstance(row, int)
            self.assertIsInstance(col, int)
            self.assertIsInstance(is_mine, bool)
            self.assertTrue(0 <= row < game.rows)
            self.assertTrue(0 <= col < game.cols)

    def test_input_output_data(self):
        # Тест работы с входными/выходными данными
        input_file = Path("data/sample_input.json")
        if input_file.exists():
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.assertIn('rows', data)
            self.assertIn('cols', data)
            self.assertIn('mines', data)
            self.assertIn('level', data)

            game = Game(data['rows'], data['cols'], data['mines'])
            self.assertEqual(game.rows, data['rows'])
            self.assertEqual(game.cols, data['cols'])
            self.assertEqual(game.mines, data['mines'])

    def test_game_with_records(self):
        # Тест игры с рекордами
        game = Game(8, 8, 9)
        game.start()

        # Имитируем игру
        for r in range(game.rows):
            for c in range(game.cols):
                if not game.is_game_over and not game.is_won:
                    game.click(r, c)

        if game.is_won:
            elapsed = game.timer.get_elapsed()
            self.records_manager.add_records("TestPlayer", elapsed, 8, 8, 9)

            records = self.records_manager.load_records()
            self.assertGreater(len(records), 0)
            self.assertEqual(records[0]['player'], "TestPlayer")
            self.assertEqual(records[0]['rows'], 8)
            self.assertEqual(records[0]['cols'], 8)
            self.assertEqual(records[0]['mines'], 9)

    def test_records_persistence(self):
        # Тест сохранения рекордов между сессиями
        self.records_manager.add_records("Player1", 60, 9, 9, 10)

        # Создаем новый менеджер
        new_manager = RecordsManager()
        new_manager.records_file = self.records_file

        records = new_manager.load_records()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]['player'], "Player1")


if __name__ == '__main__':
    unittest.main()