import tkinter as tk
from tkinter import ttk
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.player = "X"
        self.computer = "O"
        self.game_over = False
        self.scores = {"X": 0, "O": 0}
        self.buttons = []
        self.mainframe = None
        self.menu_frame = None
        self.current_mode = None

        self.setup_styles()
        self.setup_main_menu()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Helvetica', 12), padding=5)
        style.configure('Game.TButton', font=('Helvetica', 20, 'bold'))
        style.configure('TLabel', font=('Helvetica', 12))
        style.configure('Title.TLabel', font=('Helvetica', 16, 'bold'))

    def setup_main_menu(self):
        if self.mainframe:
            self.mainframe.destroy()
        if self.menu_frame:
            self.menu_frame.destroy()

        self.menu_frame = ttk.Frame(self.root, padding="20 20 20 20")
        self.menu_frame.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        ttk.Label(self.menu_frame, text="Tic Tac Toe", style='Title.TLabel').grid(column=0, row=0, pady=(0, 20))
        ttk.Button(self.menu_frame, text="Player vs Player", command=self.start_pvp_game).grid(column=0, row=1, pady=10, sticky=(tk.E, tk.W))
        ttk.Button(self.menu_frame, text="Player vs Computer", command=self.start_pvc_game).grid(column=0, row=2, pady=10, sticky=(tk.E, tk.W))
        ttk.Button(self.menu_frame, text="Exit", command=self.root.quit).grid(column=0, row=3, pady=10, sticky=(tk.E, tk.W))

        self.menu_frame.columnconfigure(0, weight=1)
        self.root.geometry("300x300")

    def start_pvp_game(self):
        self.current_mode = "PvP"
        self.menu_frame.destroy()
        self.setup_game_ui()

    def start_pvc_game(self):
        self.current_mode = "PvC"
        self.menu_frame.destroy()
        self.setup_game_ui()

    def setup_game_ui(self):
        self.mainframe = ttk.Frame(self.root, padding="20 20 20 20")
        self.mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.create_game_board()
        self.create_control_buttons()
        self.create_score_display()
        self.create_winner_label()

        self.root.geometry("350x450")

    def create_game_board(self):
        self.buttons = []
        for i in range(3):
            for j in range(3):
                button = ttk.Button(self.mainframe, text=" ", style='Game.TButton', 
                                    command=lambda row=i, col=j: self.turn(row, col))
                button.grid(column=j, row=i, sticky="nsew", padx=2, pady=2)
                self.buttons.append(button)
                self.mainframe.columnconfigure(j, weight=1)
                self.mainframe.rowconfigure(i, weight=1)

    def create_control_buttons(self):
        ttk.Button(self.mainframe, text="Reset", command=self.reset_game).grid(column=0, row=3, pady=10, sticky=(tk.E, tk.W))
        ttk.Button(self.mainframe, text="Main Menu", command=self.return_to_main_menu).grid(column=2, row=3, pady=10, sticky=(tk.E, tk.W))

    def create_score_display(self):
        self.player1_score = tk.StringVar(value=f"Player X: {self.scores['X']}")
        self.player2_score = tk.StringVar(value=f"Player O: {self.scores['O']}")

        ttk.Label(self.mainframe, textvariable=self.player1_score).grid(column=0, row=4, sticky=tk.W)
        ttk.Label(self.mainframe, textvariable=self.player2_score).grid(column=2, row=4, sticky=tk.E)

    def create_winner_label(self):
        self.winner_label = ttk.Label(self.mainframe, text="")
        self.winner_label.grid(column=0, row=5, columnspan=3)

    def turn(self, row, col):
        if self.game_over:
            return

        button = self.buttons[row * 3 + col]
        if button['text'] != " ":
            return

        button['text'] = self.player

        if self.check_winner():
            self.game_over = True
            self.update_scores()
            self.winner_label['text'] = f"Player {self.player} wins!"
        elif self.is_board_full():
            self.game_over = True
            self.winner_label['text'] = "It's a tie!"
        else:
            self.player = "O" if self.player == "X" else "X"
            if self.current_mode == "PvC" and self.player == self.computer:
                self.root.after(500, self.computer_turn)

    def computer_turn(self):
        best_score = float('-inf')
        best_move = None
        for i in range(9):
            if self.buttons[i]['text'] == " ":
                self.buttons[i]['text'] = self.computer
                score = self.minimax(0, False, float('-inf'), float('inf'))
                self.buttons[i]['text'] = " "
                if score > best_score:
                    best_score = score
                    best_move = i

        if best_move is not None:
            self.buttons[best_move]['text'] = self.computer
            if self.check_winner():
                self.game_over = True
                self.update_scores()
                self.winner_label['text'] = "Computer wins!"
            elif self.is_board_full():
                self.game_over = True
                self.winner_label['text'] = "It's a tie!"
            else:
                self.player = "X"

    def minimax(self, depth, is_maximizing, alpha, beta):
        if self.check_winner():
            return 1 if is_maximizing else -1
        if self.is_board_full():
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for i in range(9):
                if self.buttons[i]['text'] == " ":
                    self.buttons[i]['text'] = self.computer
                    score = self.minimax(depth + 1, False, alpha, beta)
                    self.buttons[i]['text'] = " "
                    best_score = max(score, best_score)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if self.buttons[i]['text'] == " ":
                    self.buttons[i]['text'] = "X"
                    score = self.minimax(depth + 1, True, alpha, beta)
                    self.buttons[i]['text'] = " "
                    best_score = min(score, best_score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
            return best_score

    def check_winner(self):
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]

        for a, b, c in win_combinations:
            if (self.buttons[a]['text'] == self.buttons[b]['text'] == self.buttons[c]['text'] != " "):
                return True

        return False

    def is_board_full(self):
        return all(button['text'] != " " for button in self.buttons)

    def update_scores(self):
        self.scores[self.player] += 1
        self.player1_score.set(f"Player X: {self.scores['X']}")
        self.player2_score.set(f"Player O: {self.scores['O']}")

    def reset_game(self):
        for button in self.buttons:
            button['text'] = " "
        self.player = "X"
        self.game_over = False
        self.winner_label['text'] = ""
        if self.current_mode == "PvC" and random.choice([True, False]):
            self.computer_turn()

    def return_to_main_menu(self):
        self.mainframe.destroy()
        self.buttons.clear()
        self.scores = {"X": 0, "O": 0}
        self.setup_main_menu()

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
