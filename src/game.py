from typing import Optional, Tuple
from src.board import Board
from src.algorithm import Algorithm
from src.timer import Timer

class Game:
    def __init__(self, rows:int, cols: int, mines: int):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = Board(rows, cols, mines)
        self.timer = Timer()
        self.is_game_over = False
        self.is_won = False
        self.flags_count = 0
    def start(self) -> None:
        self.timer.start()
    def restart(self, rows: Optional[int] = None,
                cols: Optional[int] = None,
                mines: Optional[int] = None,) ->None:
        if rows is None:
            rows = self.rows
        if cols is None:
            cols = self.cols
        if mines is None:
            mines = self.mines
            self.__init__(rows, cols, mines)
    def click(self, row: int, col:int) -> bool:
        #lmb
        if self.is_game_over or self.is_won:
            return False
        cell = self.board.get_cell(row,col)
        if not cell:
            return False
        if cell.is_flagged:
            return False
        #rmb
        if self.board.first_click:
            self.board.place_mines(row, col)
            self.board.first_click = False
            self.start()
            #press on mine
        if cell.is_mine:
            self._game_over(row, col)
            return False
        #open cell with help bfs
        Algorithm.bfs_reveal(self.board,row,col)
        #check win
        if self._check_win():
            self.is_won = True
            self.timer.stop()
            return True
        return True
    def flag(self, row:int, col:int) -> bool:
        if self.is_game_over or self.is_won:
            return False
        cell = self.board.get_cell(row, col)
        if not cell or cell.is_revealed:
            return False
        if cell.toggle_flag():
            self.flags_count += 1 if cell.is_flagged else -1
            return True
        return False
    def get_hint(self)-> Optional[Tuple[int,int,bool]]:
        if self.is_game_over or self.is_won:
            return None
        return Algorithm.deduce_hint(self.board)
    def _game_over(self, row: int, col: int) -> None:
        self.is_game_over = True
        self.timer.stop()
        #open all mines
        self.board.reveal_all_mines()
    def _check_win(self) -> bool:
        for cell in self.board.get_all_cells():
            if not cell.is_mine and not cell.is_revealed:
                return False
        return True
