import tkinter as tk
from tkinter import simpledialog, messagebox
import random
import time

class SlidingPuzzle:
    def __init__(self, root):
        self.root = root
        self.root.title("Sliding Puzzle")

        # Prompt for grid size
        self.grid_size = self.ask_grid_size()

        # Initialize puzzle state
        self.tile_size = 100
        self.empty_tile = self.grid_size * self.grid_size - 1
        self.tiles = self.generate_tiles()
        self.moves = 0
        self.start_time = None
        self.timer_running = False

        # Initialize GUI
        self.create_widgets()
        self.shuffle_tiles()

    def ask_grid_size(self):
        size = simpledialog.askinteger("Grid Size", "Choose grid size (3 or 4):", initialvalue=4, minvalue=3, maxvalue=4)
        return size

    def generate_tiles(self):
        if self.grid_size == 3:
            return list(range(1, 9)) + [0]  # 3x3 grid, tiles 1-8 and empty space 0
        elif self.grid_size == 4:
            return list(range(1, 16)) + [0]  # 4x4 grid, tiles 1-15 and empty space 0

    def create_widgets(self):
        # Create canvas for puzzle
        self.canvas = tk.Canvas(self.root, width=self.tile_size * self.grid_size, height=self.tile_size * self.grid_size, bg="brown")
        self.canvas.pack()

        # Create label for moves
        self.moves_label = tk.Label(self.root, text=f"Moves: {self.moves}")
        self.moves_label.pack()

        # Create label for timer
        self.timer_label = tk.Label(self.root, text="Time: 0:00")
        self.timer_label.pack()

        self.draw_tiles()

    def draw_tiles(self):
        self.canvas.delete("all")
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                index = i * self.grid_size + j
                tile_number = self.tiles[index]
                if tile_number != 0:
                    x = j * self.tile_size
                    y = i * self.tile_size
                    # Draw tile with brown background, black outline and number
                    self.canvas.create_rectangle(x, y, x + self.tile_size, y + self.tile_size, fill="brown", outline="black")
                    self.canvas.create_text(x + self.tile_size / 2, y + self.tile_size / 2, text=str(tile_number), font=("Arial", 24), fill="black")

        self.canvas.bind("<Button-1>", self.on_tile_click)

    def on_tile_click(self, event):
        if not self.timer_running:
            self.start_time = time.time()
            self.timer_running = True
            self.update_timer()
        
        x, y = event.x // self.tile_size, event.y // self.tile_size
        index = y * self.grid_size + x
        empty_index = self.tiles.index(0)
        empty_x, empty_y = empty_index % self.grid_size, empty_index // self.grid_size

        if (abs(empty_x - x) == 1 and empty_y == y) or (abs(empty_y - y) == 1 and empty_x == x):
            self.tiles[empty_index], self.tiles[index] = self.tiles[index], self.tiles[empty_index]
            self.moves += 1
            self.moves_label.config(text=f"Moves: {self.moves}")
            self.draw_tiles()
            if self.is_solved():
                self.stop_timer()
                messagebox.showinfo("Congratulations!", f"You solved the puzzle in {self.moves} moves and {self.get_elapsed_time()}!")

    def shuffle_tiles(self):
        random.shuffle(self.tiles)
        while not self.is_solvable() or self.is_solved():
            random.shuffle(self.tiles)
        self.draw_tiles()

    def is_solvable(self):
        inversions = 0
        one_d_tiles = [tile for tile in self.tiles if tile != 0]
        for i in range(len(one_d_tiles)):
            for j in range(i + 1, len(one_d_tiles)):
                if one_d_tiles[i] > one_d_tiles[j]:
                    inversions += 1
        if self.grid_size % 2 == 1:
            return inversions % 2 == 0
        empty_row = self.tiles.index(0) // self.grid_size
        return (inversions + empty_row) % 2 == 0

    def is_solved(self):
        correct_tiles = list(range(1, self.grid_size * self.grid_size)) + [0]
        return self.tiles == correct_tiles

    def update_timer(self):
        if self.timer_running:
            elapsed_time = time.time() - self.start_time
            minutes, seconds = divmod(int(elapsed_time), 60)
            self.timer_label.config(text=f"Time: {minutes}:{seconds:02d}")
            self.root.after(1000, self.update_timer)

    def stop_timer(self):
        self.timer_running = False

    def get_elapsed_time(self):
        if self.start_time:
            elapsed_time = time.time() - self.start_time
            minutes, seconds = divmod(int(elapsed_time), 60)
            return f"{minutes}:{seconds:02d}"
        return "0:00"

if __name__ == "__main__":
    root = tk.Tk()
    app = SlidingPuzzle(root)
    root.mainloop()
