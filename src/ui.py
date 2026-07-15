import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from typing import Optional
from src.game import Game
from src.records import RecordsManager
from src.config import *

class MinesweeperUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Сапёр")
        self.root.resizable(False, False)

        # default settings
        self.rows = DEFAULT_ROWS
        self.cols = DEFAULT_COLS
        self.mines = DEFAULT_MINES
        self.cell_size = 30
        self.current_preset = "Любитель"

        self.game: Optional[Game] = None
        self.buttons = []
        self.flag_mode = False
        self.records_manager = RecordsManager()

        self._create_menu()
        self._create_toolbar()
        self._create_board()
        self.new_game()

    def _create_menu(self) -> None:
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # game menu
        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="New Game", command=self.new_game)

        # difficult
        difficulty_menu = tk.Menu(game_menu, tearoff=0)
        game_menu.add_cascade(label="Difficulty", menu=difficulty_menu)
        for preset_name in PRESETS.keys():
            difficulty_menu.add_command(
                label=preset_name,
                command=lambda p=preset_name: self._set_preset(p)
            )
        game_menu.add_separator()
        game_menu.add_command(label="Settings", command=self._show_settings)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.root.quit)

        # hint
        hint_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Hints", menu=hint_menu)
        hint_menu.add_command(label="Get Hint", command=self._get_hint)

        # records
        records_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Records", menu=records_menu)
        records_menu.add_command(label="Show Records", command=self._show_records)

    def _create_toolbar(self) -> None:
        toolbar = tk.Frame(self.root, relief=tk.RAISED, bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # difficult button
        self.preset_buttons = {}
        for preset_name in PRESETS.keys():
            btn = tk.Button(
                toolbar,
                text=preset_name,
                command=lambda p=preset_name: self._set_preset(p)
            )
            btn.pack(side=tk.LEFT, padx=2)
            self.preset_buttons[preset_name] = btn

        # splitter
        tk.Frame(toolbar, width=2, relief=tk.SUNKEN, bd=1).pack(side=tk.LEFT, padx=5, pady=2)

        # flag indicator
        self.flags_label = tk.Label(toolbar, text="[F]: 0", font=('Arial', 12))
        self.flags_label.pack(side=tk.LEFT, padx=10)

        # flag mode button
        self.flag_btn = tk.Button(toolbar, text="[H] Flag Mode",
                                  command=self._toggle_flag_mode)
        self.flag_btn.pack(side=tk.LEFT, padx=5)

        # timer
        self.timer_label = tk.Label(toolbar, text="[T] 0", font=('Arial', 12))
        self.timer_label.pack(side=tk.RIGHT, padx=10)

        # new game button
        new_game_btn = tk.Button(toolbar, text="New Game", command=self.new_game)
        new_game_btn.pack(side=tk.RIGHT, padx=5)

        # level indicator
        self.level_label = tk.Label(
            toolbar,
            text=f"Level: {self.current_preset}",
            font=('Arial', 10, 'bold'),
            fg='blue'
        )
        self.level_label.pack(side=tk.RIGHT, padx=10)

        self._update_preset_buttons()

    def _set_preset(self, preset_name: str) -> None:
        #set difficult
        if preset_name in PRESETS:
            preset = PRESETS[preset_name]
            self.rows = preset["rows"]
            self.cols = preset["cols"]
            self.mines = preset["mines"]
            self.current_preset = preset_name
            self.level_label.config(text=f"Level: {preset_name}")
            self._update_preset_buttons()
            self._create_board()
            self.new_game()

    def _update_preset_buttons(self) -> None:
        for name, btn in self.preset_buttons.items():
            if name == self.current_preset:
                btn.config(bg="lightblue", relief=tk.SUNKEN)
            else:
                btn.config(bg="#d9d9d9", relief=tk.RAISED)

    def _create_board(self) -> None:
        #create board
        if hasattr(self, 'board_frame'):
            self.board_frame.destroy()

        # calc cell size
        self.cell_size = min(
            40,
            WINDOW_MAX_WIDTH // self.cols,
            WINDOW_MAX_HEIGHT // self.rows
        )
        self.cell_size = max(20, self.cell_size)

        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(pady=10)

        self.buttons = []
        for r in range(self.rows):
            row_buttons = []
            for c in range(self.cols):
                btn = tk.Button(
                    self.board_frame,
                    width=2,
                    height=1,
                    font=('Arial', max(8, self.cell_size // 3), 'bold'),
                    relief=tk.RAISED,
                    bd=2
                )
                btn.grid(row=r, column=c, padx=1, pady=1)
                btn.bind('<Button-1>', lambda e, row=r, col=c: self._on_left_click(row, col))
                btn.bind('<Button-3>', lambda e, row=r, col=c: self._on_right_click(row, col))
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

    def new_game(self) -> None:
        #new game
        self.game = Game(self.rows, self.cols, self.mines)
        self.game.start()
        self.flag_mode = False
        self.flag_btn.config(text="[H] Flag Mode")
        self._update_board()
        self._update_timer()

    def _update_board(self) -> None:
        #update board
        if not self.game:
            return

        self._update_timer()

        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.game.board.get_cell(r, c)
                btn = self.buttons[r][c]

                if cell.is_revealed:
                    if cell.is_mine:
                        btn.config(text="*", bg="red", state="disabled")
                    else:
                        btn.config(state="disabled", relief=tk.SUNKEN)
                        if cell.adjacent_mines > 0:
                            btn.config(text=str(cell.adjacent_mines),
                                       fg=self._get_color(cell.adjacent_mines))
                        else:
                            btn.config(text="")
                else:
                    btn.config(state="normal", relief=tk.RAISED)
                    if cell.is_flagged:
                        btn.config(text="F", bg="lightblue")
                    else:
                        btn.config(text="", bg="#d9d9d9")

        self.flags_label.config(text=f"[F]: {self.game.flags_count}")

    def _update_timer(self) -> None:
        if self.game and self.game.timer:
            elapsed = self.game.timer.get_elapsed()
            self.timer_label.config(text=f"[T] {elapsed}")
            if not self.game.is_game_over and not self.game.is_won:
                self.root.after(1000, self._update_timer)

    def _on_left_click(self, row: int, col: int) -> None:
        if not self.game or self.game.is_game_over or self.game.is_won:
            return

        cell = self.game.board.get_cell(row, col)
        if not cell or cell.is_revealed:
            return

        if self.flag_mode:
            self.game.flag(row, col)
        else:
            if cell.is_flagged:
                return
            self.game.click(row, col)

        self._update_board()
        self._check_game_status()

    def _on_right_click(self, row: int, col: int) -> None:
        if not self.game or self.game.is_game_over or self.game.is_won:
            return

        if not self.flag_mode:
            self.game.flag(row, col)
            self._update_board()

    def _toggle_flag_mode(self) -> None:
        self.flag_mode = not self.flag_mode
        self.flag_btn.config(text="[H] Flag Mode (ON)" if self.flag_mode
                            else "[H] Flag Mode")

    def _get_hint(self) -> None:
        if not self.game:
            return

        hint = self.game.get_hint()
        if hint:
            row, col, is_mine = hint
            btn = self.buttons[row][col]
            if is_mine:
                btn.config(bg="orange")
                messagebox.showinfo("Hint",
                    f"Cell ({row + 1}, {col + 1}) contains a mine!")
            else:
                btn.config(bg="lightgreen")
                messagebox.showinfo("Hint",
                    f"Cell ({row + 1}, {col + 1}) is safe!")
            self.root.after(1000, lambda: self._update_board())
        else:
            messagebox.showinfo("Hint", "No hints available")

    def _get_color(self, num: int) -> str:
        colors = {1: 'blue', 2: 'green', 3: 'red', 4: 'darkblue',
                 5: 'darkred', 6: 'cyan', 7: 'black', 8: 'gray'}
        return colors.get(num, 'black')

    def _check_game_status(self) -> None:
        if self.game.is_game_over:
            self._update_board()
            messagebox.showinfo("Game Over", "You lost")
            self._save_record_if_needed()
        elif self.game.is_won:
            self._update_board()
            messagebox.showinfo("Congratulations!", "You won!")
            self._save_record_if_needed()

    def _save_record_if_needed(self) -> None:
        if self.game.is_won:
            elapsed = self.game.timer.get_elapsed()
            if elapsed > 0:
                player_name = simpledialog.askstring("Record",
                    f"Your time: {elapsed} seconds!\nEnter your name:")
                if player_name:
                    self.records_manager.add_records(
                        player_name, elapsed, self.rows, self.cols, self.mines
                    )
                    self._show_records()

    def _show_settings(self) -> None:
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("300x250")

        tk.Label(settings_window, text="Rows:").grid(row=0, column=0, padx=5, pady=5)
        rows_entry = tk.Entry(settings_window)
        rows_entry.insert(0, str(self.rows))
        rows_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(settings_window, text="Cols:").grid(row=1, column=0, padx=5, pady=5)
        cols_entry = tk.Entry(settings_window)
        cols_entry.insert(0, str(self.cols))
        cols_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(settings_window, text="Mines:").grid(row=2, column=0, padx=5, pady=5)
        mines_entry = tk.Entry(settings_window)
        mines_entry.insert(0, str(self.mines))
        mines_entry.grid(row=2, column=1, padx=5, pady=5)

        def apply_settings():
            try:
                rows = int(rows_entry.get())
                cols = int(cols_entry.get())
                mines = int(mines_entry.get())

                if rows < MIN_ROWS or rows > MAX_ROWS:
                    raise ValueError(f"Rows from {MIN_ROWS} to {MAX_ROWS}")
                if cols < MIN_COLS or cols > MAX_COLS:
                    raise ValueError(f"Cols from {MIN_COLS} to {MAX_COLS}")
                if mines < MIN_MINES or mines > rows * cols * 0.8:
                    raise ValueError(f"Mines from {MIN_MINES} to {int(rows * cols * 0.8)}")

                self.rows = rows
                self.cols = cols
                self.mines = mines
                self.current_preset = "Custom"
                self.level_label.config(text="Level: Custom")
                self._update_preset_buttons()
                settings_window.destroy()
                self._create_board()
                self.new_game()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        apply_btn = tk.Button(settings_window, text="Apply", command=apply_settings)
        apply_btn.grid(row=3, column=0, columnspan=2, pady=20)

    def _show_records(self) -> None:
        records = self.records_manager.load_records()
        records_window = tk.Toplevel(self.root)
        records_window.title("Records Table")
        records_window.geometry("600x400")

        tree = ttk.Treeview(records_window,
                            columns=("Player", "Time", "Size", "Mines", "Date"),
                            show="headings")
        tree.heading("Player", text="Player")
        tree.heading("Time", text="Time (s)")
        tree.heading("Size", text="Size")
        tree.heading("Mines", text="Mines")
        tree.heading("Date", text="Date")
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for record in records[:MAX_RECORDS]:
            tree.insert("", "end", values=(
                record['player'],
                record['time'],
                f"{record['rows']}x{record['cols']}",
                record['mines'],
                record['date'][:19] if 'date' in record else ""
            ))

    def run(self) -> None:
        self.root.mainloop()