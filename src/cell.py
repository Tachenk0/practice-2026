class Cell:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0

    def reveal(self) -> bool:
        if not self.is_flagged and not self.is_revealed:
            self.is_revealed = True
            return True
        return False

    def toggle_flag(self) -> bool:
        if not self.is_revealed:
            self.is_flagged = not self.is_flagged
            return True
        return False

    def __str__(self) -> str:
        if self.is_revealed:
            if self.is_mine:
                return "*"
            return str(self.adjacent_mines) if self.adjacent_mines > 0 else " "
        if self.is_flagged:
            return "F"
        return "■"