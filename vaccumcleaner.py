import tkinter as tk
import random
from tkinter import font

class VacuumCleanerGUI:
    def __init__(self, master, rows=6, cols=8):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.cell_size = 40
        self.speed = 500  # ms
        self.running = False
        self.paused = False
        self.moves = 0
        self.cleaned = 0
        self.coverage = 0
        self.path = []
        self.vacuum_pos = [0, 0]
        self.floor = []
        self.algorithm = tk.StringVar(value="Snake")
        self.bold_font = font.Font(weight="bold", size=11)
        self.create_widgets()
        self.reset_floor()

    def create_widgets(self):
        # Main frame for controls
        self.control_frame = tk.Frame(self.master, bd=2, relief=tk.RIDGE, bg="#f0f4ff", padx=10, pady=8)
        self.control_frame.grid(row=0, column=1, sticky="ns", rowspan=2, padx=10, pady=10)
        # Algorithm
        tk.Label(self.control_frame, text="Algorithm:", bg="#f0f4ff").grid(row=0, column=0, sticky="w")
        algo_menu = tk.OptionMenu(self.control_frame, self.algorithm, "Snake", "Spiral")
        algo_menu.grid(row=0, column=1, sticky="ew", pady=2)
        # Grid size
        tk.Label(self.control_frame, text="Rows:", bg="#f0f4ff").grid(row=1, column=0, sticky="w")
        self.rows_entry = tk.Entry(self.control_frame, width=3)
        self.rows_entry.insert(0, str(self.rows))
        self.rows_entry.grid(row=1, column=1, sticky="ew", pady=2)
        tk.Label(self.control_frame, text="Cols:", bg="#f0f4ff").grid(row=2, column=0, sticky="w")
        self.cols_entry = tk.Entry(self.control_frame, width=3)
        self.cols_entry.insert(0, str(self.cols))
        self.cols_entry.grid(row=2, column=1, sticky="ew", pady=2)
        self.apply_btn = tk.Button(self.control_frame, text="Apply Grid Size", command=self.apply_grid_size)
        self.apply_btn.grid(row=3, column=0, columnspan=2, pady=4, sticky="ew")
        # Speed slider
        tk.Label(self.control_frame, text="Speed (ms):", bg="#f0f4ff").grid(row=4, column=0, sticky="w")
        self.speed_scale = tk.Scale(self.control_frame, from_=200, to=2000, orient=tk.HORIZONTAL, length=120, command=self.set_speed, bg="#f0f4ff")
        self.speed_scale.set(self.speed)
        self.speed_scale.grid(row=4, column=1, pady=2)
        # Buttons
        self.start_btn = tk.Button(self.control_frame, text="Start", command=self.start, width=10)
        self.start_btn.grid(row=5, column=0, pady=4)
        self.pause_btn = tk.Button(self.control_frame, text="Pause/Resume", command=self.pause, width=10)
        self.pause_btn.grid(row=5, column=1, pady=4)
        self.reset_btn = tk.Button(self.control_frame, text="Reset", command=self.reset_floor, width=10)
        self.reset_btn.grid(row=6, column=0, pady=4)
        self.quit_btn = tk.Button(self.control_frame, text="Quit", command=self.master.quit, width=10)
        self.quit_btn.grid(row=6, column=1, pady=4)
        # Statistics
        self.stats_label = tk.Label(self.control_frame, text="", font=self.bold_font, bg="#f0f4ff", pady=6)
        self.stats_label.grid(row=7, column=0, columnspan=2, sticky="ew")
        # Legend
        legend = tk.Frame(self.control_frame, bg="#f0f4ff")
        legend.grid(row=8, column=0, columnspan=2, pady=6)
        tk.Label(legend, text="Legend:", font=self.bold_font, bg="#f0f4ff").grid(row=0, column=0, columnspan=2, sticky="w")
        tk.Label(legend, text="  ", bg="blue", width=2).grid(row=1, column=0)
        tk.Label(legend, text="Vacuum", bg="#f0f4ff").grid(row=1, column=1, sticky="w")
        tk.Label(legend, text="  ", bg="red", width=2).grid(row=2, column=0)
        tk.Label(legend, text="Dirty", bg="#f0f4ff").grid(row=2, column=1, sticky="w")
        tk.Label(legend, text="  ", bg="lightgreen", width=2).grid(row=3, column=0)
        tk.Label(legend, text="Cleaned", bg="#f0f4ff").grid(row=3, column=1, sticky="w")
        tk.Label(legend, text="  ", bg="white", width=2, relief=tk.SUNKEN).grid(row=4, column=0)
        tk.Label(legend, text="Untouched", bg="#f0f4ff").grid(row=4, column=1, sticky="w")
        # Canvas
        self.canvas = tk.Canvas(self.master, width=self.cols*self.cell_size, height=self.rows*self.cell_size, bd=2, relief=tk.GROOVE, bg="#eaf0fa")
        self.canvas.grid(row=0, column=0, rowspan=2, padx=10, pady=10)

    def set_speed(self, val):
        self.speed = int(val)

    def apply_grid_size(self):
        try:
            rows = int(self.rows_entry.get())
            cols = int(self.cols_entry.get())
            if 2 <= rows <= 20 and 2 <= cols <= 20:
                self.rows = rows
                self.cols = cols
                self.canvas.config(width=self.cols*self.cell_size, height=self.rows*self.cell_size)
                self.reset_floor()
        except ValueError:
            pass

    def reset_floor(self):
        self.running = False
        self.paused = False
        self.moves = 0
        self.cleaned = 0
        self.coverage = 0
        self.path = []
        self.vacuum_pos = [0, 0]
        self.floor = [[{'dirty': random.random() > 0.6, 'visited': False} for _ in range(self.cols)] for _ in range(self.rows)]
        self.update_canvas()
        self.update_stats()

    def update_canvas(self):
        self.canvas.delete("all")
        for r in range(self.rows):
            for c in range(self.cols):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                cell = self.floor[r][c]
                color = "white"
                if r == self.vacuum_pos[0] and c == self.vacuum_pos[1]:
                    color = "blue"
                elif cell['dirty']:
                    color = "red"
                elif cell['visited']:
                    color = "lightgreen"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#555")
                if r == self.vacuum_pos[0] and c == self.vacuum_pos[1]:
                    self.canvas.create_text((x1+x2)//2, (y1+y2)//2, text="V", fill="white", font=("Arial", 16, "bold"))
        self.master.update()

    def update_stats(self):
        total_cells = self.rows * self.cols
        visited_cells = sum(cell['visited'] for row in self.floor for cell in row)
        self.coverage = int((visited_cells / total_cells) * 100)
        self.stats_label.config(text=f"Moves: {self.moves}    Cleaned: {self.cleaned}    Coverage: {self.coverage}%")

    def start(self):
        if not self.running:
            self.running = True
            self.paused = False
            self.master.after(self.speed, self.step)

    def pause(self):
        if self.running:
            self.paused = not self.paused
            if not self.paused:
                self.master.after(self.speed, self.step)

    def step(self):
        if not self.running or self.paused:
            return
        r, c = self.vacuum_pos
        cell = self.floor[r][c]
        cleaned_this_step = 0
        if cell['dirty']:
            cell['dirty'] = False
            cleaned_this_step = 1
        cell['visited'] = True
        self.moves += 1
        self.cleaned += cleaned_this_step
        self.update_stats()
        self.update_canvas()
        next_pos = self.get_next_position(r, c)
        if next_pos:
            self.vacuum_pos = next_pos
            self.master.after(self.speed, self.step)
        else:
            self.running = False

    def get_next_position(self, r, c):
        algo = self.algorithm.get().lower()
        if algo == "snake":
            # Snake pattern
            if r % 2 == 0:
                if c < self.cols - 1:
                    return [r, c + 1]
                elif r < self.rows - 1:
                    return [r + 1, c]
            else:
                if c > 0:
                    return [r, c - 1]
                elif r < self.rows - 1:
                    return [r + 1, c]
            return None
        elif algo == "spiral":
            visited = [[cell['visited'] for cell in row] for row in self.floor]
            dirs = [(0,1),(1,0),(0,-1),(-1,0)]
            dir_idx = getattr(self, 'spiral_dir', 0)
            pos = [r, c]
            for _ in range(4):
                dr, dc = dirs[dir_idx]
                nr, nc = pos[0]+dr, pos[1]+dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols and not visited[nr][nc]:
                    self.spiral_dir = dir_idx
                    return [nr, nc]
                dir_idx = (dir_idx + 1) % 4
            return None
        else:
            return None

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Vacuum Cleaner Simulator (Enhanced GUI)")
    app = VacuumCleanerGUI(root)
    root.mainloop()