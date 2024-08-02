import tkinter as tk
from tkinter import messagebox

class MissionariesCannibalsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Missionaries and Cannibals")

        # Initialize state
        self.initial_state = (3, 3, 0, 0, 'left')  # (m_left, c_left, m_right, c_right, boat)
        self.reset_game()

        # Create the canvas for drawing
        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        # Draw the initial game state
        self.draw_game()

        # Control buttons
        self.move_button = tk.Button(root, text="Move", command=self.move)
        self.move_button.pack(side=tk.LEFT, padx=10)

        self.undo_button = tk.Button(root, text="Undo", command=self.undo)
        self.undo_button.pack(side=tk.LEFT, padx=10)

        self.quit_button = tk.Button(root, text="Quit", command=root.quit)
        self.quit_button.pack(side=tk.LEFT, padx=10)

        # Input fields for move
        self.missionaries_to_move = tk.StringVar(value='0')
        self.cannibals_to_move = tk.StringVar(value='0')

        tk.Label(root, text="Missionaries to move:").pack(side=tk.LEFT, padx=5)
        tk.Entry(root, textvariable=self.missionaries_to_move, width=3).pack(side=tk.LEFT, padx=5)

        tk.Label(root, text="Cannibals to move:").pack(side=tk.LEFT, padx=5)
        tk.Entry(root, textvariable=self.cannibals_to_move, width=3).pack(side=tk.LEFT, padx=5)

    def reset_game(self):
        self.m_left, self.c_left, self.m_right, self.c_right, self.boat = self.initial_state
        self.history = []

    def draw_game(self):
        self.canvas.delete("all")  # Clear the canvas

        # Draw river
        self.canvas.create_rectangle(50, 200, 550, 220, fill="blue")

        # Draw boat
        boat_x = 50 if self.boat == 'left' else 500
        self.canvas.create_rectangle(boat_x, 180, boat_x + 40, 200, fill="brown")
        self.canvas.create_text(boat_x + 20, 190, text="Boat", fill="white")

        # Draw missionaries and cannibals on the left side
        self.draw_people(100, 150, self.m_left, self.c_left, "left")

        # Draw missionaries and cannibals on the right side
        self.draw_people(400, 150, self.m_right, self.c_right, "right")

        # Check for win condition
        if self.m_right == 3 and self.c_right == 3:
            messagebox.showinfo("Congratulations", "You won the game!")

    def draw_people(self, x, y, missionaries, cannibals, side):
        for i in range(missionaries):
            self.canvas.create_oval(x, y - i * 30, x + 20, y - i * 30 + 20, fill="white", outline="black")
            self.canvas.create_text(x + 10, y - i * 30 + 10, text="M", fill="black")

        for i in range(cannibals):
            self.canvas.create_oval(x + 30, y - i * 30, x + 50, y - i * 30 + 20, fill="green", outline="black")
            self.canvas.create_text(x + 40, y - i * 30 + 10, text="C", fill="black")

        # Draw labels
        if side == "left":
            self.canvas.create_text(x + 10, y + 20, text=f"{missionaries} Missionaries", fill="black")
            self.canvas.create_text(x + 40, y + 20, text=f"{cannibals} Cannibals", fill="black")
        else:
            self.canvas.create_text(x + 10, y + 20, text=f"{missionaries} Missionaries", fill="black")
            self.canvas.create_text(x + 40, y + 20, text=f"{cannibals} Cannibals", fill="black")

    def move(self):
        try:
            m_to_move = int(self.missionaries_to_move.get())
            c_to_move = int(self.cannibals_to_move.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid integers for missionaries and cannibals.")
            return

        if m_to_move < 0 or c_to_move < 0:
            messagebox.showerror("Invalid Input", "Number of missionaries and cannibals to move cannot be negative.")
            return

        if self.boat == 'left':
            if (self.m_left >= m_to_move and self.c_left >= c_to_move and
                self.is_valid_state(self.m_left - m_to_move, self.c_left - c_to_move,
                                    self.m_right + m_to_move, self.c_right + c_to_move)):
                self.m_left -= m_to_move
                self.c_left -= c_to_move
                self.m_right += m_to_move
                self.c_right += c_to_move
                self.boat = 'right'
            else:
                messagebox.showerror("Invalid Move", "Cannot make this move. It would leave missionaries in danger or exceed available numbers.")
                return
        else:
            if (self.m_right >= m_to_move and self.c_right >= c_to_move and
                self.is_valid_state(self.m_left + m_to_move, self.c_left + c_to_move,
                                    self.m_right - m_to_move, self.c_right - c_to_move)):
                self.m_left += m_to_move
                self.c_left += c_to_move
                self.m_right -= m_to_move
                self.c_right -= c_to_move
                self.boat = 'left'
            else:
                messagebox.showerror("Invalid Move", "Cannot make this move. It would leave missionaries in danger or exceed available numbers.")
                return

        self.history.append((self.m_left, self.c_left, self.m_right, self.c_right, self.boat))
        self.draw_game()

    def undo(self):
        if self.history:
            self.m_left, self.c_left, self.m_right, self.c_right, self.boat = self.history.pop()
            self.draw_game()
        else:
            messagebox.showwarning("No Move to Undo", "No previous move to undo.")

    def is_valid_state(self, m_left, c_left, m_right, c_right):
        """
        Check if the current state is valid.
        No side should ever have more cannibals than missionaries.
        """
        if (m_left < 0 or m_left > 3 or c_left < 0 or c_left > 3 or 
            m_right < 0 or m_right > 3 or c_right < 0 or c_right > 3):
            return False
        
        if (m_left > 0 and m_left < c_left) or (m_right > 0 and m_right < c_right):
            return False
        
        return True

if __name__ == "__main__":
    root = tk.Tk()
    app = MissionariesCannibalsGUI(root)
    root.mainloop()
