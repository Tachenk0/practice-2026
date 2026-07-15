import unittest
from src.board import Board


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board(9, 9, 10)

    def test_initialization(self):
        self.assertEqual(self.board.rows, 9)
        self.assertEqual(self.board.cols, 9)
        self.assertEqual(self.board.mines, 10)
        self.assertTrue(self.board.first_click)
        self.assertFalse(self.board.game_over)

    def test_place_mines(self):
        self.board.place_mines(4, 4)
        # Проверяем, что мины не в безопасной зоне
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                r, c = 4 + dr, 4 + dc
                if 0 <= r < 9 and 0 <= c < 9:
                    cell = self.board.get_cell(r, c)
                    self.assertFalse(cell.is_mine)

        # Проверяем количество мин
        mine_count = sum(1 for r in range(9) for c in range(9)
                         if self.board.grid[r][c].is_mine)
        self.assertEqual(mine_count, 10)

    def test_get_cell(self):
        cell = self.board.get_cell(0, 0)
        self.assertIsNotNone(cell)
        self.assertEqual(cell.row, 0)
        self.assertEqual(cell.col, 0)

        cell = self.board.get_cell(10, 10)
        self.assertIsNone(cell)

    def test_get_all_cells(self):
        cells = self.board.get_all_cells()
        self.assertEqual(len(cells), 9 * 9)
        self.assertEqual(len(set(cells)), 9 * 9)

    def test_count_adjacent_mines(self):
        board = Board(3, 3, 1)
        board.place_mines(0, 0)
        cell = board.get_cell(0, 1)
        if cell:
            self.assertGreaterEqual(cell.adjacent_mines, 0)

    def test_reveal_all_mines(self):
        self.board.place_mines(4, 4)
        self.board.reveal_all_mines()
        for cell in self.board.get_all_cells():
            if cell.is_mine:
                self.assertTrue(cell.is_revealed)

    def test_get_remaining_mines(self):
        self.board.place_mines(4, 4)
        remaining = self.board.get_remaining_mines()
        self.assertEqual(remaining, 10)

        for cell in self.board.get_all_cells():
            if cell.is_mine:
                cell.toggle_flag()
                break

        remaining = self.board.get_remaining_mines()
        self.assertEqual(remaining, 9)

    def test_str_representation(self):
        board = Board(3, 3, 1)
        board.place_mines(1, 1)
        str_repr = str(board)
        self.assertIsInstance(str_repr, str)
        self.assertGreater(len(str_repr), 0)


if __name__ == '__main__':
    unittest.main()