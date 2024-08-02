import tkinter as tk
from tkinter import messagebox
import math

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.current_player = 'X'
        self.buttons = [[None, None, None] for _ in range(3)]
        self.create_widgets()

    def create_widgets(self):
        for row in range(3):
            for col in range(3):
                button = tk.Button(self.root, text=' ', font=('Arial', 24, 'bold'), width=5, height=2,
                                   bg='light blue', fg='black', 
                                   borderwidth=2, relief='solid',
                                   command=lambda r=row, c=col: self.on_button_click(r, c))
                button.grid(row=row, column=col, padx=5, pady=5)
                self.buttons[row][col] = button

    def on_button_click(self, row, col):
        if self.current_player == 'X':  # Only allow move if it's player's turn
            button = self.buttons[row][col]
            if button['text'] == ' ':
                button['text'] = self.current_player
                if self.check_winner(self.current_player):
                    self.show_winner(self.current_player)
                elif self.check_tie():
                    self.show_tie()
                else:
                    self.current_player = 'O'
                    self.root.after(500, self.computer_move)  # Delay to allow player to see move

    def computer_move(self):
        best_move = self.find_best_move()
        if best_move:
            row, col = best_move
            self.buttons[row][col]['text'] = self.current_player
            if self.check_winner(self.current_player):
                self.show_winner(self.current_player)
            elif self.check_tie():
                self.show_tie()
            else:
                self.current_player = 'X'

    def find_best_move(self):
        best_val = -math.inf
        best_move = None
        for row in range(3):
            for col in range(3):
                if self.buttons[row][col]['text'] == ' ':
                    self.buttons[row][col]['text'] = 'O'
                    move_val = self.minimax(False, -math.inf, math.inf)
                    self.buttons[row][col]['text'] = ' '
                    if move_val > best_val:
                        best_move = (row, col)
                        best_val = move_val
        return best_move

    def minimax(self, is_max, alpha, beta):
        if self.check_winner('O'):
            return 10
        if self.check_winner('X'):
            return -10
        if self.check_tie():
            return 0

        if is_max:
            best = -math.inf
            for row in range(3):
                for col in range(3):
                    if self.buttons[row][col]['text'] == ' ':
                        self.buttons[row][col]['text'] = 'O'
                        best = max(best, self.minimax(False, alpha, beta))
                        self.buttons[row][col]['text'] = ' '
                        alpha = max(alpha, best)
                        if beta <= alpha:
                            break
            return best
        else:
            best = math.inf
            for row in range(3):
                for col in range(3):
                    if self.buttons[row][col]['text'] == ' ':
                        self.buttons[row][col]['text'] = 'X'
                        best = min(best, self.minimax(True, alpha, beta))
                        self.buttons[row][col]['text'] = ' '
                        beta = min(beta, best)
                        if beta <= alpha:
                            break
            return best

    def check_winner(self, player):
        # Check rows, columns and diagonals
        for i in range(3):
            if all(self.buttons[i][j]['text'] == player for j in range(3)) or \
               all(self.buttons[j][i]['text'] == player for j in range(3)):
                return True
        if all(self.buttons[i][i]['text'] == player for i in range(3)) or \
           all(self.buttons[i][2-i]['text'] == player for i in range(3)):
            return True
        return False

    def check_tie(self):
        return all(self.buttons[row][col]['text'] != ' ' for row in range(3) for col in range(3))

    def show_winner(self, player):
        messagebox.showinfo("Game Over", f"Player {player} wins!")
        self.reset_game()

    def show_tie(self):
        messagebox.showinfo("Game Over", "It's a tie!")
        self.reset_game()

    def reset_game(self):
        for row in range(3):
            for col in range(3):
                self.buttons[row][col]['text'] = ' '
        self.current_player = 'X'

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
