import unittest
from src.board import Board
from src.algorithm import Algorithm


class TestAlgorithm(unittest.TestCase):
    #Тесты для алгоритмов

    def setUp(self):
        #Создание поля перед каждым тестом
        self.board = Board(9, 9, 10)
        self.board.place_mines(4, 4)

    def test_bfs_reveal(self):
        #тест BFS на пустой клетке
        # Ищем пустую клетку
        found_empty = False
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                cell = self.board.get_cell(r, c)
                if cell and not cell.is_mine and cell.adjacent_mines == 0:
                    # Запоминаем, что нашли пустую клетку
                    found_empty = True

                    # Сохраняем состояние до BFS
                    initial_revealed = sum(1 for cell in self.board.get_all_cells()
                                           if cell.is_revealed)

                    # Запускаем BFS
                    revealed = Algorithm.bfs_reveal(self.board, r, c)

                    # Проверяем, что открылось больше клеток
                    final_revealed = sum(1 for cell in self.board.get_all_cells()
                                         if cell.is_revealed)
                    self.assertGreater(final_revealed, initial_revealed)
                    self.assertGreater(len(revealed), 0)
                    break
            if found_empty:
                break

        if not found_empty:
            self.skipTest("Нет пустых клеток для теста BFS")

    def test_bfs_does_not_reveal_flagged(self):
        #тест BFS не открывает клетки с флагами
        # Ищем клетку для теста
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                cell = self.board.get_cell(r, c)
                if cell and not cell.is_mine and not cell.is_revealed:
                    # Ставим флаг
                    cell.toggle_flag()

                    # Пытаемся открыть через BFS
                    Algorithm.bfs_reveal(self.board, r, c)

                    # Проверяем, что клетка не открылась
                    self.assertFalse(cell.is_revealed)
                    self.assertTrue(cell.is_flagged)
                    break

    def test_deduce_hint(self):
        #тест алгоритма дедукции
        # Создаем специальное поле для теста дедукции
        board = Board(3, 3, 1)
        board.place_mines(1, 1)

        # Открываем клетку с известным числом
        cell = board.get_cell(0, 0)
        if cell:
            cell.is_revealed = True
            cell.adjacent_mines = 1

        # Получаем подсказку
        hint = Algorithm.deduce_hint(board)

        # Если подсказка есть, проверяем её формат
        if hint:
            row, col, is_mine = hint
            self.assertIsInstance(row, int)
            self.assertIsInstance(col, int)
            self.assertIsInstance(is_mine, bool)
            self.assertTrue(0 <= row < board.rows)
            self.assertTrue(0 <= col < board.cols)

    def test_bfs_returns_cells(self):
        #тест что BFS возвращает список открытых клеток
        # Ищем безопасную клетку
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                cell = self.board.get_cell(r, c)
                if cell and not cell.is_mine:
                    revealed = Algorithm.bfs_reveal(self.board, r, c)
                    self.assertIsInstance(revealed, list)
                    if len(revealed) > 0:
                        self.assertIsInstance(revealed[0], tuple)
                        self.assertEqual(len(revealed[0]), 2)
                    break


if __name__ == '__main__':
    unittest.main()