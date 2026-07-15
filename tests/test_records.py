import unittest
import tempfile
import os
from src.records import RecordsManager
from src.config import MAX_RECORDS


class TestRecordsManager(unittest.TestCase):
    # Тесты для управления рекордами

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.records_file = os.path.join(self.temp_dir, 'records.json')

        self.manager = RecordsManager()
        self.manager.records_file = self.records_file
        self.manager._ensure_file_exists()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_add_record(self):
        # Тест добавления рекорда
        result = self.manager.add_records("Player1", 60, 9, 9, 10)
        self.assertTrue(result)

        records = self.manager.load_records()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]['player'], "Player1")
        self.assertEqual(records[0]['time'], 60)
        self.assertEqual(records[0]['rows'], 9)
        self.assertEqual(records[0]['cols'], 9)
        self.assertEqual(records[0]['mines'], 10)

    def test_add_multiple_records(self):
        # Тест добавления нескольких рекордов для РАЗНЫХ полей
        self.manager.add_records("Player1", 60, 9, 9, 10)
        self.manager.add_records("Player2", 45, 8, 8, 9)  # Другая комбинация
        self.manager.add_records("Player3", 30, 16, 16, 40)  # Еще другая

        records = self.manager.load_records()
        # Должно быть 3 записи (разные комбинации)
        self.assertEqual(len(records), 3)

        # Проверяем, что все игроки есть
        players = [r['player'] for r in records]
        self.assertIn("Player1", players)
        self.assertIn("Player2", players)
        self.assertIn("Player3", players)

    def test_add_multiple_same_preset(self):
        # Тест добавления нескольких рекордов для ОДИНАКОВОГО поля
        self.manager.add_records("Player1", 60, 9, 9, 10)
        self.manager.add_records("Player2", 45, 9, 9, 10)
        self.manager.add_records("Player3", 30, 9, 9, 10)

        records = self.manager.load_records()
        # Должна остаться только лучшая запись (Player3)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]['player'], "Player3")
        self.assertEqual(records[0]['time'], 30)

    def test_load_records(self):
        # Тест загрузки рекордов
        self.manager.add_records("Player1", 60, 9, 9, 10)

        records = self.manager.load_records()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]['player'], "Player1")

    def test_ensure_file_exists(self):
        # Тест создания файла
        self.assertTrue(os.path.exists(self.records_file))
        import json
        with open(self.records_file, 'r') as f:
            data = json.load(f)
            self.assertEqual(data, [])

    def test_get_best_time(self):
        # Тест получения лучшего времени
        self.manager.add_records("Player1", 60, 9, 9, 10)
        self.manager.add_records("Player2", 45, 9, 9, 10)
        self.manager.add_records("Player3", 30, 9, 9, 10)

        best = self.manager.get_best_time(9, 9, 10)
        self.assertEqual(best, 30)

        # Несуществующая комбинация
        best = self.manager.get_best_time(8, 8, 9)
        self.assertIsNone(best)

    def test_get_records_by_preset(self):
        # Тест получения рекордов по пресету
        self.manager.add_records("Player1", 60, 9, 9, 10)
        self.manager.add_records("Player2", 45, 8, 8, 9)
        self.manager.add_records("Player3", 30, 9, 9, 10)

        records = self.manager.get_records_by_preset(9, 9, 10)
        # Должна быть только лучшая запись для этого пресета
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]['player'], "Player3")
        self.assertEqual(records[0]['time'], 30)

        records = self.manager.get_records_by_preset(8, 8, 9)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]['player'], "Player2")
        self.assertEqual(records[0]['time'], 45)

    def test_max_records_limit(self):
        # Тест ограничения на количество рекордов
        # Добавляем записи для разных полей
        for i in range(MAX_RECORDS + 5):
            self.manager.add_records(f"Player{i}", 100 - i, i + 1, i + 1, i + 1)

        records = self.manager.load_records()
        self.assertLessEqual(len(records), MAX_RECORDS)


if __name__ == '__main__':
    unittest.main()