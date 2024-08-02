import tkinter as tk
from collections import deque

class DFSVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("DFS Visualization")
        
        # Define graph
        self.graph = {
            'A': {'B', 'C'},
            'B': {'A', 'D', 'E'},
            'C': {'A', 'F', 'G'},
            'D': {'B'},
            'E': {'B', 'H'},
            'F': {'C'},
            'G': {'C'},
            'H': {'E'}
        }
        
        self.stack = deque()
        self.visited = set()
        
        self.node_positions = {
            'A': (100, 50),
            'B': (50, 150),
            'C': (150, 150),
            'D': (30, 250),
            'E': (70, 250),
            'F': (130, 250),
            'G': (170, 250),
            'H': (110, 300)
        }
        
        # Create canvas for drawing
        self.canvas = tk.Canvas(root, width=400, height=400, bg='white')
        self.canvas.pack(pady=10)
        
        self.start_button = tk.Button(root, text="Start DFS", command=self.start_dfs)
        self.start_button.pack(pady=10)
    
        self.draw_graph()
    
    def draw_graph(self):
        self.canvas.delete("all")
        
        # Draw edges
        for node, neighbors in self.graph.items():
            x1, y1 = self.node_positions[node]
            for neighbor in neighbors:
                x2, y2 = self.node_positions[neighbor]
                self.canvas.create_line(x1, y1, x2, y2, fill='black')
        
        # Draw nodes
        for node, (x, y) in self.node_positions.items():
            self.canvas.create_oval(x-15, y-15, x+15, y+15, fill='lightblue', outline='black')
            self.canvas.create_text(x, y, text=node, font=('Helvetica', 12))
    
    def start_dfs(self):
        self.clear_labels()
        self.stack = deque(['A'])
        self.visited = set()
        self.dfs()
    
    def dfs(self):
        if not self.stack:
            return
        
        node = self.stack.pop()
        
        if node not in self.visited:
            self.visited.add(node)
            self.display_node(node)
            self.highlight_node(node)
            # Add nodes to stack (DFS: LIFO order)
            self.stack.extend(self.graph[node] - self.visited)
            self.root.after(1000, self.dfs)  # Delay of 1000 milliseconds (1 second) for visualization
    
    def display_node(self, node):
        # This method can be used to update the status or label of the current node
        pass
    
    def highlight_node(self, node):
        x, y = self.node_positions[node]
        self.canvas.create_oval(x-15, y-15, x+15, y+15, fill='lightgreen', outline='black', tags="highlight")
        self.canvas.create_text(x, y, text=node, font=('Helvetica', 12, 'bold'), fill='black', tags="highlight")
    
    def clear_labels(self):
        self.canvas.delete("highlight")
        self.draw_graph()

# Create the Tkinter window
if __name__ == "__main__":
    root = tk.Tk()
    app = DFSVisualizer(root)
    root.mainloop()
