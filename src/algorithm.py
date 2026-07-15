from collections import deque
from typing import List, Optional, Tuple
from src.board import Board


class Algorithm:


    @staticmethod
    def bfs_reveal(board: Board, start_row: int, start_col: int) -> List[Tuple[int, int]]:

        if not board or not board.get_cell(start_row, start_col):
            return []

        revealed = []
        queue = deque([(start_row, start_col)])
        visited = set([(start_row, start_col)])

        while queue:
            row, col = queue.popleft()
            cell = board.get_cell(row, col)

            if not cell or cell.is_revealed or cell.is_flagged:
                continue

            # Открываем клетку
            cell.reveal()
            revealed.append((row, col))

            # Если клетка пустая (0 соседних мин), добавляем соседей
            if cell.adjacent_mines == 0 and not cell.is_mine:
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        r, c = row + dr, col + dc
                        if 0 <= r < board.rows and 0 <= c < board.cols:
                            if (r, c) not in visited:
                                neighbor = board.get_cell(r, c)
                                if neighbor and not neighbor.is_flagged:
                                    visited.add((r, c))
                                    queue.append((r, c))

        return revealed

    @staticmethod
    def deduce_hint(board: Board) -> Optional[Tuple[int, int, bool]]:

        for r in range(board.rows):
            for c in range(board.cols):
                cell = board.get_cell(r, c)
                if not cell or not cell.is_revealed or cell.is_mine:
                    continue

                # Получаем информацию о соседях
                flagged = 0
                unrevealed = []

                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < board.rows and 0 <= nc < board.cols:
                            neighbor = board.get_cell(nr, nc)
                            if neighbor:
                                if neighbor.is_flagged:
                                    flagged += 1
                                elif not neighbor.is_revealed:
                                    unrevealed.append((nr, nc))

                # Если все мины найдены, остальные клетки безопасны
                if cell.adjacent_mines == flagged and unrevealed:
                    for nr, nc in unrevealed:
                        neighbor = board.get_cell(nr, nc)
                        if neighbor and neighbor.is_mine:
                            return (nr, nc, True)  # Это мина
                        return (nr, nc, False)  # Это безопасно

                # Если количество флагов на 1 меньше мин,
                # и есть только одна неоткрытая клетка - это мина
                if cell.adjacent_mines == flagged + 1 and len(unrevealed) == 1:
                    nr, nc = unrevealed[0]
                    return (nr, nc, True)  # Это мина

        return None  # Подсказок нет