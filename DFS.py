import tkinter as tk
import random
from tkinter import font


class VacuumCleanerDFS:
    def __init__(self, master, rows=6, cols=8):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.cell_size = 42
        self.speed = 500
        self.running = False
        self.paused = False
        self.moves = 0
        self.cleaned = 0
        self.coverage = 0
        self.vacuum_pos = [0, 0]
        self.floor = []
        self.bold_font = font.Font(weight="bold", size=12)
        self.stats_font = font.Font(weight="bold", size=13)
        self.create_widgets()
        self.reset_floor()


    def create_widgets(self):
        self.master.configure(bg="#eaf0fa")
        self.main_frame = tk.Frame(self.master, bg="#eaf0fa")
        self.main_frame.pack(fill="both", expand=True, padx=16, pady=12)
        self.left_frame = tk.Frame(self.main_frame, bg="#eaf0fa")
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        self.canvas_frame = tk.Frame(self.left_frame, bd=2, relief=tk.SUNKEN, bg="#444")
        self.canvas_frame.pack(padx=8, pady=(8,0))
        self.canvas = tk.Canvas(self.canvas_frame, width=self.cols*self.cell_size, height=self.rows*self.cell_size, bg="#eaf0fa", highlightthickness=0)
        self.canvas.pack()
        info = (
            "DFS Vacuum Cleaner:\n"
            "- The robot uses Depth-First Search to visit and clean all cells.\n"
            "- Blue: Robot position | Red: Dirty | Light Green: Cleaned | White: Untouched\n"
            "- Adjust grid size and speed, then press Start."
        )
        self.info_label = tk.Label(self.left_frame, text=info, bg="#eaf0fa", fg="#222", font=("Arial", 11), justify="left", anchor="w", padx=8)
        self.info_label.pack(pady=(10,0), fill="x")
        legend = tk.Frame(self.left_frame, bg="#eaf0fa")
        legend.pack(anchor="w", pady=(8,0), padx=8)
        tk.Label(legend, text="Legend:", font=self.bold_font, bg="#eaf0fa").grid(row=0, column=0, sticky="w", columnspan=2)
        tk.Label(legend, text="  ", bg="blue", width=2).grid(row=1, column=0)
        tk.Label(legend, text="Vacuum", bg="#eaf0fa").grid(row=1, column=1, sticky="w")
        tk.Label(legend, text="  ", bg="red", width=2).grid(row=2, column=0)
        tk.Label(legend, text="Dirty", bg="#eaf0fa").grid(row=2, column=1, sticky="w")
        tk.Label(legend, text="  ", bg="lightgreen", width=2).grid(row=3, column=0)
        tk.Label(legend, text="Cleaned", bg="#eaf0fa").grid(row=3, column=1, sticky="w")
        tk.Label(legend, text="  ", bg="white", width=2, relief=tk.SUNKEN).grid(row=4, column=0)
        tk.Label(legend, text="Untouched", bg="#eaf0fa").grid(row=4, column=1, sticky="w")
        self.right_frame = tk.Frame(self.main_frame, bg="#f0f4ff", bd=2, relief=tk.RIDGE, padx=14, pady=10)
        self.right_frame.grid(row=0, column=1, sticky="ns", padx=(16,8), pady=0)
        tk.Label(self.right_frame, text="Algorithm:", bg="#f0f4ff", font=("Arial", 11)).grid(row=0, column=0, sticky="w")
        tk.Label(self.right_frame, text="DFS (Depth-First Search)", fg="blue", bg="#f0f4ff",
                 font=("Arial", 11, "bold")).grid(row=0, column=1, sticky="ew", pady=(0,6))
        tk.Label(self.right_frame, text="Rows:", bg="#f0f4ff").grid(row=1, column=0, sticky="w")
        self.rows_entry = tk.Entry(self.right_frame, width=3)
        self.rows_entry.insert(0, str(self.rows))
        self.rows_entry.grid(row=1, column=1, sticky="ew")
        tk.Label(self.right_frame, text="Cols:", bg="#f0f4ff").grid(row=2, column=0, sticky="w")
        self.cols_entry = tk.Entry(self.right_frame, width=3)
        self.cols_entry.insert(0, str(self.cols))
        self.cols_entry.grid(row=2, column=1, sticky="ew")
        self.apply_btn = tk.Button(self.right_frame, text="Apply Grid Size", command=self.apply_grid_size)
        self.apply_btn.grid(row=3, column=0, columnspan=2, pady=5, sticky="ew")
        tk.Label(self.right_frame, text="Speed (ms):", bg="#f0f4ff").grid(row=4, column=0, sticky="w")
        self.speed_scale = tk.Scale(self.right_frame, from_=200, to=2000, orient=tk.HORIZONTAL, length=120, command=self.set_speed, bg="#f0f4ff")
        self.speed_scale.set(self.speed)
        self.speed_scale.grid(row=4, column=1, pady=2)
        self.start_btn = tk.Button(self.right_frame, text="Start", command=self.start, width=10)
        self.start_btn.grid(row=5, column=0, pady=5)
        self.pause_btn = tk.Button(self.right_frame, text="Pause/Resume", command=self.pause, width=10)
        self.pause_btn.grid(row=5, column=1, pady=5)
        self.reset_btn = tk.Button(self.right_frame, text="Reset", command=self.reset_floor, width=10)
        self.reset_btn.grid(row=6, column=0, pady=5)
        self.quit_btn = tk.Button(self.right_frame, text="Quit", command=self.master.quit, width=10)
        self.quit_btn.grid(row=6, column=1, pady=5)
        self.stats_label = tk.Label(self.right_frame, text="", font=self.stats_font, bg="#f0f4ff", pady=8)
        self.stats_label.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(18,0))


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
        self.vacuum_pos = [0, 0]
        self.floor = [[{'dirty': random.random() > 0.6, 'visited': False} for _ in range(self.cols)] for _ in range(self.rows)]
        self.dfs_stack = []
        self.visited_dfs = set()
        self.update_canvas()
        self.update_stats()


    def update_canvas(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(1, 1, self.cols*self.cell_size-2, self.rows*self.cell_size-2, outline="#222", width=2)
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
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#666")
                if r == self.vacuum_pos[0] and c == self.vacuum_pos[1]:
                    self.canvas.create_text((x1+x2)//2, (y1+y2)//2, text="V", fill="white", font=("Arial", 16, "bold"))
        self.master.update()


    def update_stats(self):
        total_cells = self.rows * self.cols
        visited_cells = sum(cell['visited'] for row in self.floor for cell in row)
        self.coverage = int((visited_cells / total_cells) * 100)
        self.stats_label.config(
            text=f"Moves: {self.moves}    Cleaned: {self.cleaned}    Coverage: {self.coverage}%"
        )


    def start(self):
        if not self.running:
            self.running = True
            self.paused = False
            self.dfs_stack = [tuple(self.vacuum_pos)]
            self.visited_dfs = set()
            self.master.after(self.speed, self.step)


    def pause(self):
        if self.running:
            self.paused = not self.paused
            if not self.paused:
                self.master.after(self.speed, self.step)


    def step(self):
        if not self.running or self.paused:
            return
        if not self.dfs_stack:
            self.running = False
            return
        r, c = self.dfs_stack.pop()
        if (r, c) in self.visited_dfs:
            self.master.after(self.speed, self.step)
            return
        self.vacuum_pos = [r, c]
        cell = self.floor[r][c]
        cleaned_this_step = 0
        if cell['dirty']:
            cell['dirty'] = False
            cleaned_this_step = 1
        cell['visited'] = True
        self.moves += 1
        self.cleaned += cleaned_this_step
        self.visited_dfs.add((r, c))
        self.update_stats()
        self.update_canvas()
        for dr, dc in [(-1,0),(0,1),(1,0),(0,-1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols and not self.floor[nr][nc]['visited']:
                self.dfs_stack.append((nr, nc))
        self.master.after(self.speed, self.step)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("DFS Vacuum Cleaner Simulator")
    app = VacuumCleanerDFS(root)
    root.mainloop()
