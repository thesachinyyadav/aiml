import tkinter as tk
from tkinter import messagebox, ttk
import heapq
import math

LOCATIONS = {
    "Warehouse": (100, 100),
    "Mall": (300, 100),
    "Hospital": (500, 100),
    "School": (100, 300),
    "Office": (300, 300),
    "Park": (500, 300),
    "Station": (100, 500),
    "Airport": (300, 500)
}

ROADS = {
    ("Warehouse", "Mall"): 15,
    ("Warehouse", "School"): 10,
    ("Mall", "Hospital"): 12,
    ("Mall", "Office"): 8,
    ("Hospital", "Park"): 10,
    ("School", "Office"): 5,
    ("School", "Station"): 20,
    ("Office", "Park"): 7,
    ("Office", "Airport"): 12,
    ("Park", "Airport"): 8,
    ("Station", "Airport"): 15
}

class DeliveryPathfinder:
    def __init__(self, root):
        self.root = root
        root.title("Delivery Route Optimizer - A* Algorithm")
        root.geometry("900x650")
        
        self.location_list = sorted(LOCATIONS.keys())
        self.src_var = tk.StringVar(value="Warehouse")
        self.dst_var = tk.StringVar(value="Airport")
        
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        title_frame = tk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        tk.Label(title_frame, text="Delivery Route Optimizer", 
                font=("Arial", 16, "bold")).pack()
        
        control_frame = tk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(control_frame, text="From:").pack(side=tk.LEFT)
        self.src_combo = ttk.Combobox(control_frame, textvariable=self.src_var, 
                                     values=self.location_list, width=12)
        self.src_combo.pack(side=tk.LEFT, padx=(5, 20))
        
        tk.Label(control_frame, text="To:").pack(side=tk.LEFT)
        self.dst_combo = ttk.Combobox(control_frame, textvariable=self.dst_var, 
                                     values=self.location_list, width=12)
        self.dst_combo.pack(side=tk.LEFT, padx=(5, 20))
        
        tk.Button(control_frame, text="Find Fastest Route", 
                 command=self.find_route, bg="lightgreen").pack(side=tk.LEFT, padx=(20, 10))
        tk.Button(control_frame, text="Clear", 
                 command=self.clear_map).pack(side=tk.LEFT)
        
        self.canvas = tk.Canvas(main_frame, width=600, height=600, bg="lightblue", relief=tk.SUNKEN, bd=2)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        info_frame = tk.Frame(main_frame, width=280)
        info_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        info_frame.pack_propagate(False)
        
        tk.Label(info_frame, text="Route Analysis:", font=("Arial", 12, "bold")).pack(anchor="w")
        self.info_text = tk.Text(info_frame, height=30, width=35, wrap=tk.WORD)
        scrollbar = tk.Scrollbar(info_frame, orient=tk.VERTICAL, command=self.info_text.yview)
        self.info_text.config(yscrollcommand=scrollbar.set)
        self.info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.draw_map()
        
    def draw_map(self):
        self.canvas.delete("all")
        
        for (loc1, loc2), time in ROADS.items():
            x1, y1 = LOCATIONS[loc1]
            x2, y2 = LOCATIONS[loc2]
            
            self.canvas.create_line(x1, y1, x2, y2, width=3, fill="gray", tags="road")
            
            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            self.canvas.create_rectangle(mid_x-15, mid_y-8, mid_x+15, mid_y+8, 
                                       fill="white", outline="", tags="time_bg")
            self.canvas.create_text(mid_x, mid_y, text=f"{time}min", fill="blue", 
                                   font=("Arial", 9, "bold"), tags="time")
        
        for location, (x, y) in LOCATIONS.items():
            self.canvas.create_oval(x-25, y-25, x+25, y+25, fill="yellow", 
                                   outline="black", width=2, tags="location")
            self.canvas.create_text(x, y-35, text=location, font=("Arial", 10, "bold"), tags="label")
    
    def straight_line_distance(self, loc1, loc2):
        """Calculate straight-line distance (heuristic for A*)"""
        x1, y1 = LOCATIONS[loc1]
        x2, y2 = LOCATIONS[loc2]
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return distance / 6
    
    def get_connected_locations(self, location):
        """Get all directly connected locations"""
        connections = []
        for (loc1, loc2), time in ROADS.items():
            if loc1 == location:
                connections.append((loc2, time))
            elif loc2 == location:
                connections.append((loc1, time))
        return connections
    
    def astar_pathfinding(self, start, destination):
        """A* Algorithm for finding fastest delivery route"""
        open_list = [(0, 0, start, [start])]
        visited = set()
        steps = []
        
        steps.append(f" DELIVERY ROUTE PLANNING")
        steps.append(f"From: {start} → To: {destination}")
        steps.append(f"Starting A* algorithm.\n")
        
        step_count = 1
        
        while open_list:
            estimated_time, actual_time, current_loc, path = heapq.heappop(open_list)
            
            steps.append(f"Step {step_count}:")
            steps.append(f"  Checking: {current_loc}")
            steps.append(f"  Time so far: {actual_time} min")
            steps.append(f"  Estimated total: {estimated_time:.1f} min")
            
            if current_loc == destination:
                steps.append(f"\n DESTINATION REACHED!")
                steps.append(f"Optimal route: {' → '.join(path)}")
                steps.append(f"Total delivery time: {actual_time} minutes")
                return path, actual_time, steps
            
            if current_loc in visited:
                steps.append(f"  Already visited, skipping\n")
                continue
                
            visited.add(current_loc)
            steps.append(f"  Exploring from {current_loc}...")
            
            connections = self.get_connected_locations(current_loc)
            
            for next_loc, travel_time in connections:
                if next_loc not in visited:
                    new_actual_time = actual_time + travel_time
                    heuristic_time = self.straight_line_distance(next_loc, destination)
                    new_estimated_time = new_actual_time + heuristic_time
                    
                    steps.append(f"    → {next_loc}: {travel_time}min")
                    steps.append(f"      Total time: {new_actual_time}min")
                    steps.append(f"      Estimated: {new_estimated_time:.1f}min")
                    
                    new_path = path + [next_loc]
                    heapq.heappush(open_list, (new_estimated_time, new_actual_time, next_loc, new_path))
            
            steps.append("")
            step_count += 1
        
        steps.append("No route found!")
        return None, None, steps
    
    def find_route(self):
        start = self.src_var.get()
        destination = self.dst_var.get()
        
        if start == destination:
            messagebox.showwarning("Same Location", "Start and destination are the same!")
            return
        
        self.clear_map()
        self.info_text.delete(1.0, tk.END)
        
        route, time, steps = self.astar_pathfinding(start, destination)
        
        for step in steps:
            self.info_text.insert(tk.END, step + "\n")
        
        if route:
            self.highlight_route(route)
            
            summary = f"\n{'='*35}\n"
            summary += f" DELIVERY SUMMARY:\n"
            summary += f"Route: {' → '.join(route)}\n"
            summary += f"Total Time: {time} minutes\n"
            summary += f"Stops: {len(route)-1}\n"
            summary += f"{'='*35}\n"
            
            self.info_text.insert(tk.END, summary)
            
            messagebox.showinfo("Route Found!", 
                               f"Fastest route: {' → '.join(route)}\nTime: {time} minutes")
        else:
            messagebox.showerror("No Route", "Cannot find a route between these locations!")
    
    def highlight_route(self, route):
        """Highlight the optimal route on the map"""
        for i in range(len(route) - 1):
            loc1, loc2 = route[i], route[i + 1]
            x1, y1 = LOCATIONS[loc1]
            x2, y2 = LOCATIONS[loc2]
            
            self.canvas.create_line(x1, y1, x2, y2, width=6, fill="red", tags="route")
            
            self.canvas.create_line(x2-10, y2-10, x2, y2, width=4, fill="red", tags="arrow")
            self.canvas.create_line(x2-10, y2+10, x2, y2, width=4, fill="red", tags="arrow")
        
        start_x, start_y = LOCATIONS[route[0]]
        end_x, end_y = LOCATIONS[route[-1]]
        
        self.canvas.create_oval(start_x-28, start_y-28, start_x+28, start_y+28, 
                               fill="green", outline="darkgreen", width=3, tags="start")
        self.canvas.create_text(start_x, start_y, text="START", font=("Arial", 8, "bold"), 
                               fill="white", tags="start_label")
        
        self.canvas.create_oval(end_x-28, end_y-28, end_x+28, end_y+28, 
                               fill="red", outline="darkred", width=3, tags="end")
        self.canvas.create_text(end_x, end_y, text="END", font=("Arial", 8, "bold"), 
                               fill="white", tags="end_label")
    
    def clear_map(self):
        """Clear the map and redraw"""
        self.canvas.delete("route")
        self.canvas.delete("start")
        self.canvas.delete("end")
        self.canvas.delete("start_label")
        self.canvas.delete("end_label")
        self.canvas.delete("arrow")
        self.info_text.delete(1.0, tk.END)
        self.draw_map()

def main():
    root = tk.Tk()
    app = DeliveryPathfinder(root)
    root.mainloop()

if __name__ == "__main__":
    main()