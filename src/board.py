import random
from typing import List, Optional, Tuple
from src.cell import Cell

class Board:
    def __init__(self, rows: int, cols: int, mines: int):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.grid: List[List[Cell]] = []
        self.first_click = True
        self.game_over = False
        self._init_board()

    def _init_board(self) -> None:
      #empty board
        self.grid = [[Cell(row, col) for col in range(self.cols)]
                     for row in range(self.rows)]

    def place_mines(self, safe_row: int, safe_col: int) -> None:
        # safezone after 1 click
        safe_zone = set()
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                r, c = safe_row + dr, safe_col + dc
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    safe_zone.add((r, c))

        # check mines count
        max_mines = self.rows * self.cols - len(safe_zone)
        if self.mines > max_mines:
            self.mines = max_mines

        # place mines
        positions = [(r, c) for r in range(self.rows)
                     for c in range(self.cols)
                     if (r, c) not in safe_zone]
        mine_positions = random.sample(positions, self.mines)

        for r, c in mine_positions:
            self.grid[r][c].is_mine = True

        # calculate the neighboring mines for each cell
        for r in range(self.rows):
            for c in range(self.cols):
                if not self.grid[r][c].is_mine:
                    self.grid[r][c].adjacent_mines = self._count_adjacent_mines(r, c)
    def _count_adjacent_mines(self, row: int,col: int) -> int :
        count = 0
        for dr in [-1,0,1]:
            for dc in [-1,0,1]:
                if dr == 0 and dc == 0:
                    continue
                r,c = row + dr,col + dc
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    if self.grid[r][c].is_mine:
                        count +=1
        return count
    def get_cell(self, row:int, col:int) -> Optional[Cell]:
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return None
    def get_all_cells(self) -> List[Cell]:
        return [cell for row in self.grid for cell in row]
    def get_remaining_mines(self) -> int:
        flagged = sum(1 for cell in self.get_all_cells() if cell.is_flagged)
        return self.mines - flagged
    def reveal_all_mines(self) -> None:
        #open all mines if player loose
        for cell in self.get_all_cells():
            if cell.is_mine:
                cell.is_revealed = True
    def __str__(self) -> str:
        result = " " + " ".join(str(i) for i in range(self.cols)) + "\n"
        for r in range(self.rows):
            result += f"{r}"
            for c in range(self.cols):
                result += str(self.grid[r][c]) + " "
            result += "\n"
        return result

