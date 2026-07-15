import unittest
from src.cell import Cell


class TestCell(unittest.TestCase):
    # Тесты для ячейки

    def setUp(self):
        # Создание ячейки перед каждым тестом
        self.cell = Cell(0, 0)

    def test_initial_state(self):
        # Проверка начального состояния ячейки
        self.assertEqual(self.cell.row, 0)
        self.assertEqual(self.cell.col, 0)
        self.assertFalse(self.cell.is_mine)
        self.assertFalse(self.cell.is_revealed)
        self.assertFalse(self.cell.is_flagged)
        self.assertEqual(self.cell.adjacent_mines, 0)

    def test_reveal(self):
        # Тест открытия ячейки
        # Открываем ячейку
        result = self.cell.reveal()
        self.assertTrue(result)
        self.assertTrue(self.cell.is_revealed)

        # Повторное открытие не должно работать
        result = self.cell.reveal()
        self.assertFalse(result)

    def test_toggle_flag(self):
        # Тест установки/снятия флага
        # Устанавливаем флаг
        result = self.cell.toggle_flag()
        self.assertTrue(result)
        self.assertTrue(self.cell.is_flagged)

        # Снимаем флаг
        result = self.cell.toggle_flag()
        self.assertTrue(result)
        self.assertFalse(self.cell.is_flagged)

    def test_cannot_flagged_if_revealed(self):
        # Нельзя поставить флаг на открытую ячейку
        self.cell.reveal()
        result = self.cell.toggle_flag()
        self.assertFalse(result)
        self.assertFalse(self.cell.is_flagged)

    def test_cannot_reveal_if_flagged(self):
        # Нельзя открыть ячейку с флагом
        self.cell.toggle_flag()
        result = self.cell.reveal()
        self.assertFalse(result)
        self.assertFalse(self.cell.is_revealed)

    def test_str_representation(self):
        # Тест строкового представления
        # Закрытая ячейка
        self.assertEqual(str(self.cell), "■")

        # Ячейка с флагом
        self.cell.toggle_flag()
        self.assertEqual(str(self.cell), "F")

        # Открытая пустая ячейка
        self.cell.toggle_flag()  # Снимаем флаг
        self.cell.reveal()
        self.assertEqual(str(self.cell), " ")

        # Открытая ячейка с миной
        self.cell.is_mine = True
        self.assertEqual(str(self.cell), "*")

        # Открытая ячейка с числом
        self.cell.is_mine = False
        self.cell.adjacent_mines = 3
        self.assertEqual(str(self.cell), "3")


if __name__ == '__main__':
    unittest.main()