import unittest
from src.game import Game


class TestGame(unittest.TestCase):
    #тесты для игровой логики

    def setUp(self):
        #создание игры перед каждым тестом
        self.game = Game(9, 9, 10)

    def test_initialization(self):
        #тест инициализации игры
        self.assertEqual(self.game.rows, 9)
        self.assertEqual(self.game.cols, 9)
        self.assertEqual(self.game.mines, 10)
        self.assertFalse(self.game.is_game_over)
        self.assertFalse(self.game.is_won)
        self.assertEqual(self.game.flags_count, 0)
        self.assertTrue(self.game.board.first_click)

    def test_start(self):
        #тест запуска игры
        self.game.start()
        self.assertTrue(self.game.timer.running)
        self.assertIsNotNone(self.game.timer.start_time)

    def test_first_click_places_mines(self):
        #тест первого клика размещает мины
        # До клика мины не размещены
        self.assertTrue(self.game.board.first_click)

        # Делаем клик
        self.game.click(4, 4)

        # После клика мины размещены
        self.assertFalse(self.game.board.first_click)

        # Проверяем, что мины есть
        mine_count = sum(1 for cell in self.game.board.get_all_cells()
                         if cell.is_mine)
        self.assertEqual(mine_count, 10)

    def test_click_on_safe_cell(self):
        #тест клика по безопасной клетке
        self.game.click(4, 4)

        # Проверяем, что клетка открыта
        cell = self.game.board.get_cell(4, 4)
        self.assertTrue(cell.is_revealed)

    def test_click_on_mine(self):
        #тест клика по мине
        # Сначала размещаем мины
        self.game.board.place_mines(4, 4)
        self.game.board.first_click = False

        # Ищем мину
        for r in range(self.game.rows):
            for c in range(self.game.cols):
                cell = self.game.board.get_cell(r, c)
                if cell and cell.is_mine:
                    # Кликаем по мине
                    self.game.click(r, c)
                    self.assertTrue(self.game.is_game_over)
                    self.assertTrue(cell.is_revealed)
                    return

        self.skipTest("Не найдена мина для теста")

    def test_flag(self):
        #тест установки флага
        self.game.board.place_mines(4, 4)
        self.game.board.first_click = False

        # Ищем клетку для флага
        for r in range(self.game.rows):
            for c in range(self.game.cols):
                cell = self.game.board.get_cell(r, c)
                if cell and not cell.is_mine and not cell.is_revealed:
                    # Ставим флаг
                    result = self.game.flag(r, c)
                    self.assertTrue(result)
                    self.assertTrue(cell.is_flagged)
                    self.assertEqual(self.game.flags_count, 1)

                    # Снимаем флаг
                    result = self.game.flag(r, c)
                    self.assertTrue(result)
                    self.assertFalse(cell.is_flagged)
                    self.assertEqual(self.game.flags_count, 0)
                    return

        self.skipTest("Не найдена клетка для теста флага")

    def test_cannot_click_after_game_over(self):
        #тест нельзя кликать после окончания игры
        self.game.is_game_over = True
        result = self.game.click(4, 4)
        self.assertFalse(result)

    def test_get_hint(self):
        #тест получения подсказки
        self.game.board.place_mines(4, 4)
        hint = self.game.get_hint()
        # Подсказка может быть None или кортежем
        if hint:
            row, col, is_mine = hint
            self.assertIsInstance(row, int)
            self.assertIsInstance(col, int)
            self.assertIsInstance(is_mine, bool)

    def test_restart(self):
        #тест перезапуска игры
        self.game.click(4, 4)
        old_board = self.game.board

        self.game.restart()

        self.assertNotEqual(id(self.game.board), id(old_board))
        self.assertEqual(self.game.rows, 9)
        self.assertEqual(self.game.cols, 9)
        self.assertEqual(self.game.mines, 10)
        self.assertTrue(self.game.board.first_click)


if __name__ == '__main__':
    unittest.main()