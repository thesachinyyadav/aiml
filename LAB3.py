import tkinter as tk
from tkinter import messagebox, ttk
from tkintermapview import TkinterMapView
import heapq
from collections import deque

CITIES = {
    "Bengaluru": (12.9716, 77.5946),
    "Mysuru": (12.2958, 76.6394),
    "Mandya": (12.5242, 76.8997),
    "Tumakuru": (13.3409, 77.1017),
    "Channapatna": (12.6557, 77.2177),
    "Ramanagara": (12.7217, 77.2812),
    "Hassan": (13.0063, 76.1004),
    "Chikkaballapur": (13.4355, 77.7315),
    "Nelamangala": (13.0993, 77.3962),
    "Kolar": (13.1372, 78.1297),
    "Anekal": (12.7094, 77.6972),
    "Shivamogga": (13.9299, 75.5681),
    "Davangere": (14.4644, 75.9218),
    "Hubballi": (15.3647, 75.1240),
    "Belagavi": (15.8497, 74.4977),
    "Mangaluru": (12.9141, 74.8560),
    "Udupi": (13.3409, 74.7421),
}

ROUTES = {
    ("Bengaluru", "Mandya"): {"car": (92, 105), "bus": (92, 120), "bike": (92, 130)},
    ("Mandya", "Mysuru"): {"car": (45, 50), "bus": (45, 60), "bike": (45, 65)},
    ("Bengaluru", "Tumakuru"): {"car": (70, 80), "bus": (70, 95), "bike": (70, 110)},
    ("Bengaluru", "Channapatna"): {"car": (60, 70), "bus": (60, 85), "bike": (60, 90)},
    ("Channapatna", "Ramanagara"): {"car": (15, 20), "bus": (15, 25), "bike": (15, 30)},
    ("Ramanagara", "Mandya"): {"car": (35, 45), "bus": (35, 55), "bike": (35, 60)},
    ("Bengaluru", "Hassan"): {"car": (183, 210), "bus": (183, 250), "bike": (183, 290)},
    ("Mysuru", "Hassan"): {"car": (118, 135), "bus": (118, 155), "bike": (118, 170)},
    ("Bengaluru", "Chikkaballapur"): {"car": (59, 65), "bus": (59, 80), "bike": (59, 85)},
    ("Bengaluru", "Nelamangala"): {"car": (27, 35), "bus": (27, 45), "bike": (27, 50)},
    ("Nelamangala", "Tumakuru"): {"car": (45, 52), "bus": (45, 65), "bike": (45, 70)},
    ("Bengaluru", "Kolar"): {"car": (68, 75), "bus": (68, 90), "bike": (68, 95)},
    ("Bengaluru", "Anekal"): {"car": (40, 45), "bus": (40, 55), "bike": (40, 60)},
    ("Bengaluru", "Shivamogga"): {"car": (275, 320), "bus": (275, 380), "bike": (275, 420)},
    ("Shivamogga", "Davangere"): {"car": (105, 125), "bus": (105, 150), "bike": (105, 170)},
    ("Davangere", "Hubballi"): {"car": (143, 165), "bus": (143, 180), "bike": (143, 190)},
    ("Hubballi", "Belagavi"): {"car": (102, 120), "bus": (102, 140), "bike": (102, 160)},
    ("Bengaluru", "Mangaluru"): {"car": (350, 400), "bus": (350, 430), "bike": (350, 480)},
    ("Mangaluru", "Udupi"): {"car": (58, 65), "bus": (58, 80), "bike": (58, 85)},
    ("Bengaluru", "Udupi"): {"car": (403, 460), "bus": (403, 500), "bike": (403, 550)},
}

class GPSNavigator:
    def __init__(self, root):
        self.root = root
        root.title("Karnataka GPS Map")
        root.geometry("1100x700")
        self.city_list = sorted(CITIES)
        self.src_var = tk.StringVar(value="Bengaluru")
        self.dst_var = tk.StringVar(value="Mysuru")
        self.mode_var = tk.StringVar(value="car")
        self.optimize_var = tk.StringVar(value="distance")
        self.markers, self.lines = [], []

        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        self.map_widget = TkinterMapView(main_frame, width=800, height=600, corner_radius=0)
        self.map_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.map_widget.set_zoom(7)
        self.map_widget.set_position(13.5, 76.0)

        panel = tk.Frame(main_frame, width=300)
        panel.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        tk.Label(panel, text="Source:").pack()
        self.src_combo = ttk.Combobox(panel, textvariable=self.src_var, values=self.city_list, width=22)
        self.src_combo.pack()
        tk.Label(panel, text="Destination:").pack()
        self.dst_combo = ttk.Combobox(panel, textvariable=self.dst_var, values=self.city_list, width=22)
        self.dst_combo.pack()
        tk.Label(panel, text="Mode:").pack()
        for text, value in [("Car", "car"), ("Bus", "bus"), ("Bike", "bike")]:
            ttk.Radiobutton(panel, text=text, variable=self.mode_var, value=value).pack(anchor="w")
        tk.Label(panel, text="Optimize For:").pack()
        for text, value in [("Distance", "distance"), ("Time", "time")]:
            ttk.Radiobutton(panel, text=text, variable=self.optimize_var, value=value).pack(anchor="w")
        tk.Button(panel, text="Best Route", command=self.find_best_route).pack(fill=tk.X, pady=2)
        tk.Button(panel, text="Show Alternatives", command=self.show_all_routes).pack(fill=tk.X, pady=2)
        tk.Button(panel, text="Clear Map", command=self.clear_routes).pack(fill=tk.X, pady=2)
        self.info_text = tk.Text(panel, height=18, width=36)
        self.info_text.pack(fill=tk.BOTH, expand=True)

        self.draw_all_cities()

    def draw_all_cities(self):
        for m in self.markers: m.delete()
        self.markers = [self.map_widget.set_marker(lat, lon, text=city) for city, (lat, lon) in CITIES.items()]

    def clear_routes(self):
        for l in self.lines: l.delete()
        self.lines = []
        self.info_text.delete(1.0, tk.END)
        self.draw_all_cities()

    def draw_route(self, path, color="blue", width=3):
        coords = [CITIES[city] for city in path if city in CITIES]
        if len(coords) > 1:
            line = self.map_widget.set_path(coords, color=color, width=width)
            self.lines.append(line)

    def get_neighbors(self, city):
        return [c2 if c1 == city else c1 for c1, c2 in ROUTES if city in (c1, c2)]

    def get_route_cost(self, city1, city2, mode, optimize):
        r = ROUTES.get((city1, city2)) or ROUTES.get((city2, city1))
        if not r: return None
        d, t = r[mode]
        return d if optimize == "distance" else t

    def dijkstra(self, start, end, mode, optimize):
        pq, visited = [(0, start, [start])], set()
        while pq:
            cost, city, path = heapq.heappop(pq)
            if city == end: return path, cost
            if city in visited: continue
            visited.add(city)
            for neighbor in self.get_neighbors(city):
                if neighbor in visited: continue
                rcost = self.get_route_cost(city, neighbor, mode, optimize)
                if rcost is not None:
                    heapq.heappush(pq, (cost+rcost, neighbor, path+[neighbor]))
        return None, None

    def bfs_paths(self, start, end, mode, max_paths=4):
        queue, results, seen = deque([(start, [start])]), [], set()
        while queue and len(results) < max_paths:
            city, path = queue.popleft()
            if city == end and tuple(path) not in seen:
                seen.add(tuple(path))
                results.append(path)
                continue
            if len(path) > 8: continue
            for neighbor in self.get_neighbors(city):
                if neighbor not in path:
                    queue.append((neighbor, path+[neighbor]))
        return results

    def find_best_route(self):
        self.clear_routes()
        start, end = self.src_var.get(), self.dst_var.get()
        mode, opt = self.mode_var.get(), self.optimize_var.get()
        if start == end or start not in CITIES or end not in CITIES:
            messagebox.showwarning("Invalid", "Check your city selection!")
            return
        path, cost = self.dijkstra(start, end, mode, opt)
        if path:
            self.draw_route(path, color="red", width=5)
            self.info_text.insert(tk.END, f"Best Route:\n{' → '.join(path)}\nTotal {opt.title()}: {cost}\n")
        else:
            self.info_text.insert(tk.END, "No route found. Try another city pair or mode.\n")

    def show_all_routes(self):
        self.clear_routes()
        start, end, mode = self.src_var.get(), self.dst_var.get(), self.mode_var.get()
        paths = self.bfs_paths(start, end, mode)
        colors = ["red", "blue", "green", "purple"]
        if not paths:
            self.info_text.insert(tk.END, "No alternative routes found. Try another city pair.\n")
            return
        for i, path in enumerate(paths):
            self.draw_route(path, color=colors[i%len(colors)], width=3)
            cost = sum(self.get_route_cost(path[j], path[j+1], mode, "distance") for j in range(len(path)-1))
            time = sum(self.get_route_cost(path[j], path[j+1], mode, "time") for j in range(len(path)-1))
            self.info_text.insert(tk.END, f"Route {i+1}: {' → '.join(path)}\nDistance: {cost}km, Time: {time}min\n\n")

def main():
    root = tk.Tk()
    GPSNavigator(root)
    root.mainloop()

if __name__ == "__main__":
    main()