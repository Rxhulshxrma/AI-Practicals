import tkinter as tk
from tkinter import messagebox

class WaterJugGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Water Jug Puzzle Game")

        self.create_widgets()
        self.setup_initial_state()

    def create_widgets(self):
        # Create canvas for drawing jugs
        self.canvas = tk.Canvas(self.root, width=600, height=400, bg="burlywood")
        self.canvas.pack()

        # Action Buttons
        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.pack()

        self.empty_a_button = tk.Button(self.buttons_frame, text="Empty Jug A", command=lambda: self.empty('A'), font=("Arial", 12))
        self.empty_a_button.pack(side=tk.LEFT, padx=5)

        self.empty_b_button = tk.Button(self.buttons_frame, text="Empty Jug B", command=lambda: self.empty('B'), font=("Arial", 12))
        self.empty_b_button.pack(side=tk.LEFT, padx=5)

        self.empty_c_button = tk.Button(self.buttons_frame, text="Empty Jug C", command=lambda: self.empty('C'), font=("Arial", 12))
        self.empty_c_button.pack(side=tk.LEFT, padx=5)

        self.fill_a_button = tk.Button(self.buttons_frame, text="Fill Jug A", command=lambda: self.fill('A'), font=("Arial", 12))
        self.fill_a_button.pack(side=tk.LEFT, padx=5)

        self.fill_b_button = tk.Button(self.buttons_frame, text="Fill Jug B", command=lambda: self.fill('B'), font=("Arial", 12))
        self.fill_b_button.pack(side=tk.LEFT, padx=5)

        self.pour_ab_button = tk.Button(self.buttons_frame, text="Pour A -> C", command=lambda: self.pour('A', 'C'), font=("Arial", 12))
        self.pour_ab_button.pack(side=tk.LEFT, padx=5)

        self.pour_ba_button = tk.Button(self.buttons_frame, text="Pour B -> C", command=lambda: self.pour('B', 'C'), font=("Arial", 12))
        self.pour_ba_button.pack(side=tk.LEFT, padx=5)

        self.pour_ac_button = tk.Button(self.buttons_frame, text="Pour C -> A", command=lambda: self.pour('C', 'A'), font=("Arial", 12))
        self.pour_ac_button.pack(side=tk.LEFT, padx=5)

        self.pour_bc_button = tk.Button(self.buttons_frame, text="Pour C -> B", command=lambda: self.pour('C', 'B'), font=("Arial", 12))
        self.pour_bc_button.pack(side=tk.LEFT, padx=5)

        # Target Amount
        self.canvas.create_text(300, 30, text="Water Jug Puzzle Game", font=("Arial", 24), fill="black")
        self.canvas.create_text(100, 370, text="Target Jug", font=("Arial", 14), fill="black")

    def setup_initial_state(self):
        # Jug capacities
        self.capacity_a = 5
        self.capacity_b = 3
        self.capacity_c = 8

        # Initial amounts
        self.jug_a = 0
        self.jug_b = 0
        self.jug_c = 0

        self.update_canvas()

    def update_canvas(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(50, 100, 150, 300, outline="black", fill="white")  # Jug A
        self.canvas.create_rectangle(250, 100, 350, 300, outline="black", fill="white")  # Jug B
        self.canvas.create_rectangle(450, 100, 550, 300, outline="black", fill="white")  # Jug C

        # Draw jugs
        self.draw_jug(50, 100, self.capacity_a, self.jug_a)
        self.draw_jug(250, 100, self.capacity_b, self.jug_b)
        self.draw_jug(450, 100, self.capacity_c, self.jug_c)

    def draw_jug(self, x, y, capacity, amount):
        jug_width = 100
        jug_height = 200
        water_height = jug_height * (amount / capacity)

        self.canvas.create_rectangle(x, y, x + jug_width, y + jug_height, outline="black", fill="white")
        self.canvas.create_rectangle(x, y + jug_height - water_height, x + jug_width, y + jug_height, outline="black", fill="blue")
        self.canvas.create_text(x + jug_width / 2, y + jug_height - water_height / 2, text=f"{amount} L", font=("Arial", 16), fill="black")

    def pour(self, from_jug, to_jug):
        if from_jug == 'A' and to_jug == 'C':
            amount = min(self.jug_a, self.capacity_c - self.jug_c)
            self.jug_a -= amount
            self.jug_c += amount
        elif from_jug == 'B' and to_jug == 'C':
            amount = min(self.jug_b, self.capacity_c - self.jug_c)
            self.jug_b -= amount
            self.jug_c += amount
        elif from_jug == 'C' and to_jug == 'A':
            amount = min(self.jug_c, self.capacity_a - self.jug_a)
            self.jug_c -= amount
            self.jug_a += amount
        elif from_jug == 'C' and to_jug == 'B':
            amount = min(self.jug_c, self.capacity_b - self.jug_b)
            self.jug_c -= amount
            self.jug_b += amount
        self.update_canvas()

    def empty(self, jug):
        if jug == 'A':
            self.jug_a = 0
        elif jug == 'B':
            self.jug_b = 0
        elif jug == 'C':
            self.jug_c = 0
        self.update_canvas()

    def fill(self, jug):
        if jug == 'A':
            self.jug_a = self.capacity_a
        elif jug == 'B':
            self.jug_b = self.capacity_b
        self.update_canvas()

if __name__ == "__main__":
    root = tk.Tk()
    app = WaterJugGame(root)
    root.mainloop()
