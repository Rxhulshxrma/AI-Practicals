import tkinter as tk
from tkinter import messagebox, simpledialog

class NQueensGUI:
    def __init__(self, root, size):
        self.root = root
        self.size = size
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.buttons = [[None for _ in range(size)] for _ in range(size)]
        self.create_board()

    def create_board(self):
        for i in range(self.size):
            for j in range(self.size):
                color = 'white' if (i + j) % 2 == 0 else 'gray'
                button = tk.Button(self.root, bg=color, width=4, height=2, command=lambda i=i, j=j: self.toggle_queen(i, j))
                button.grid(row=i, column=j)
                self.buttons[i][j] = button

    def toggle_queen(self, row, col):
        if self.board[row][col] == 1:
            self.board[row][col] = 0
            self.buttons[row][col].config(text='', bg=self.get_default_color(row, col))
        else:
            if not self.is_position_safe(row, col):
                messagebox.showwarning("Invalid Move", "Cannot place a queen here!")
                return
            self.board[row][col] = 1
            self.buttons[row][col].config(text='Q', bg=self.get_default_color(row, col))
        
        self.update_board_colors()
        if self.is_solution():
            messagebox.showinfo("Congratulations", f"Congratulations, you have solved the {self.size}-Queens problem!")

    def get_default_color(self, row, col):
        return 'white' if (row + col) % 2 == 0 else 'gray'

    def is_position_safe(self, row, col):
        for i in range(self.size):
            if self.board[row][i] == 1 and i != col:
                return False
            if self.board[i][col] == 1 and i != row:
                return False
        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if self.board[i][j] == 1:
                return False
        for i, j in zip(range(row, self.size, 1), range(col, -1, -1)):
            if self.board[i][j] == 1:
                return False
        for i, j in zip(range(row, -1, -1), range(col, self.size, 1)):
            if self.board[i][j] == 1:
                return False
        for i, j in zip(range(row, self.size, 1), range(col, self.size, 1)):
            if self.board[i][j] == 1:
                return False
        return True

    def solve_nq_util(self, board, col):
        if col >= self.size:
            return True
        for i in range(self.size):
            if self.is_position_safe(i, col):
                board[i][col] = 1
                if self.solve_nq_util(board, col + 1):
                    return True
                board[i][col] = 0
        return False

    def solve(self):
        if self.solve_nq_util(self.board, 0):
            self.update_board()
            messagebox.showinfo("Congratulations", f"Congratulations, you have solved the {self.size}-Queens problem!")
        else:
            messagebox.showinfo("No Solution", "No solution exists for the given board size.")

    def update_board(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 1:
                    self.buttons[i][j].config(text='Q', bg=self.get_default_color(i, j))
                else:
                    self.buttons[i][j].config(text='', bg=self.get_default_color(i, j))

    def update_board_colors(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 1 and not self.is_position_safe(i, j):
                    self.buttons[i][j].config(bg='red')
                else:
                    self.buttons[i][j].config(bg=self.get_default_color(i, j))
                if self.board[i][j] == 1:
                    self.buttons[i][j].config(text='Q')

    def is_solution(self):
        # Check if there are exactly 'size' queens on the board
        queen_count = sum(sum(row) for row in self.board)
        if queen_count != self.size:
            return False
        # Check if all queens are in safe positions
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == 1 and not self.is_position_safe(row, col):
                    return False
        return True

if __name__ == "__main__":
    root = tk.Tk()
    root.title("N-Queens Problem")
    
    # Prompt the user to choose between 4-Queens and 8-Queens problem
    size = simpledialog.askinteger("Input", "Enter the size of the board (4 or 8):", minvalue=4, maxvalue=8)
    if size not in [4, 8]:
        messagebox.showerror("Error", "Invalid size. Please restart and enter either 4 or 8.")
        root.destroy()
    else:
        gui = NQueensGUI(root, size)
        root.mainloop()
