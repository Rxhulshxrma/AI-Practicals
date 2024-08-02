import tkinter as tk
from tkinter import messagebox

class TowerOfHanoiGame:
    def __init__(self, master, num_disks):
        self.master = master
        self.master.title("Tower of Hanoi")
        self.num_disks = num_disks
        self.pegs = [[], [], []]

        for i in range(num_disks, 0, -1):
            self.pegs[0].append(i)

        self.selected_disk = None
        self.create_widgets()
        self.draw_disks()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.master, width=600, height=400, bg="white")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.peg_positions = [100, 300, 500]
        self.disk_height = 20
        self.peg_colors = ["green", "blue", "red"]
        self.disk_colors = ["orange", "yellow", "purple", "cyan", "magenta", "pink", "lime", "grey", "brown", "gold"]

    def draw_disks(self):
        self.canvas.delete("all")
        self.disk_map = {}
        for peg_index, peg in enumerate(self.pegs):
            x = self.peg_positions[peg_index]
            y = 350
            self.canvas.create_line(x, 50, x, 350, width=2, fill=self.peg_colors[peg_index])
            for disk in peg:
                width = disk * 20
                disk_color = self.disk_colors[self.num_disks - disk]  # Select color based on disk size
                disk_id = self.canvas.create_rectangle(
                    x - width / 2, y - self.disk_height, x + width / 2, y, fill=disk_color, outline="black"
                )
                self.disk_map[disk_id] = (peg_index, disk)
                y -= self.disk_height

    def on_canvas_click(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        if item and item[0] in self.disk_map:
            peg_index, disk = self.disk_map[item[0]]
            if self.pegs[peg_index][-1] == disk:
                self.selected_disk = item[0]
                self.canvas.tag_raise(self.selected_disk)

    def on_canvas_drag(self, event):
        if self.selected_disk:
            self.canvas.coords(self.selected_disk, event.x - 20, event.y - 10, event.x + 20, event.y + 10)

    def on_canvas_release(self, event):
        if self.selected_disk:
            item = self.selected_disk
            self.selected_disk = None
            peg_index = self.get_closest_peg(event.x)
            if self.is_valid_move(item, peg_index):
                self.move_disk(item, peg_index)
            else:
                self.draw_disks()

    def get_closest_peg(self, x):
        return min(range(3), key=lambda i: abs(x - self.peg_positions[i]))

    def is_valid_move(self, item, peg_index):
        _, disk = self.disk_map[item]
        return not self.pegs[peg_index] or self.pegs[peg_index][-1] > disk

    def move_disk(self, item, peg_index):
        old_peg_index, disk = self.disk_map[item]
        self.pegs[old_peg_index].remove(disk)
        self.pegs[peg_index].append(disk)
        self.draw_disks()
        self.check_win_condition()

    def check_win_condition(self):
        if len(self.pegs[2]) == self.num_disks:
            messagebox.showinfo("Congratulations", "You have solved the Tower of Hanoi!")

if __name__ == "__main__":
    root = tk.Tk()
    app = TowerOfHanoiGame(root, 3)
    root.mainloop()
