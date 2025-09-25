import pygame, math, heapq, random, time

city_positions = {
    'Bangalore': (150, 400),
    'Chennai': (650, 130),
    'Hyderabad': (420, 320),
    'Kochi': (650, 500),
    'Mumbai': (200, 150)
}
city_edges_base = {
    'Bangalore': {'Hyderabad': 4, 'Chennai': 6, 'Mumbai': 7},
    'Chennai': {'Hyderabad': 5, 'Kochi': 7, 'Bangalore': 6},
    'Hyderabad': {'Bangalore': 4, 'Chennai': 5, 'Kochi': 4, 'Mumbai': 8},
    'Kochi': {'Hyderabad': 4, 'Chennai': 7},
    'Mumbai': {'Bangalore': 7, 'Hyderabad': 8}
}

WIDTH, HEIGHT = 900, 650
CITY_RADIUS = 34
FPS = 60

BG = (235, 240, 250)
CITY = (80, 170, 255)
CITY_SELECTED = (255, 120, 100)
CITY_EXPLORED = (255, 220, 50)
CITY_CLOSED = (180, 180, 180)
ROAD = (180, 200, 220)
ROAD_BLOCKED = (220, 80, 80)
ROAD_PATH = (0, 230, 60)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("City Route Finder - A* Pathfinding")
font = pygame.font.SysFont("consolas", 26)
small_font = pygame.font.SysFont("consolas", 20)
clock = pygame.time.Clock()


def heuristic(c1, c2):
    x1, y1 = city_positions[c1]
    x2, y2 = city_positions[c2]
    return math.hypot(x2 - x1, y2 - y1)

def get_blocked_roads(city_edges, prob=0.28):
    blocked = set()
    for c, nbrs in city_edges.items():
        for n in nbrs:
            edge = tuple(sorted([c, n]))
            if random.random() < prob:
                blocked.add(edge)
    return blocked

def apply_traffic(city_edges):
    traffic_edges = {}
    for c, nbrs in city_edges.items():
        traffic_edges[c] = {}
        for n, cost in nbrs.items():
            traffic = random.uniform(1.0, 1.6)  
            traffic_edges[c][n] = round(cost * traffic, 1)
    return traffic_edges

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]

def a_star_animated(city_map, start, goal, blocked, draw_callback):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {c: float('inf') for c in city_map}
    g_score[start] = 0
    f_score = {c: float('inf') for c in city_map}
    f_score[start] = heuristic(start, goal)
    open_set_cities = set([start])
    closed_set = set()
    while open_set:
        pygame.event.pump()
        _, current = heapq.heappop(open_set)
        open_set_cities.discard(current)

        if current == goal:
            return reconstruct_path(came_from, current)

        closed_set.add(current)
        draw_callback(current, set(open_set_cities), set(closed_set))
        pygame.display.flip()
        pygame.time.delay(200)

        for neighbor, cost in city_map[current].items():
            edge = tuple(sorted([current, neighbor]))
            if edge in blocked:
                continue
            tentative_g = g_score[current] + cost
            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                if neighbor not in open_set_cities and neighbor not in closed_set:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
                    open_set_cities.add(neighbor)
    return []

def draw_map(selected=None, path=None, blocked=None, open_cities=None, closed_cities=None):
    if selected is None: selected = []
    if path is None: path = []
    if blocked is None: blocked = set()
    if open_cities is None: open_cities = set()
    if closed_cities is None: closed_cities = set()
    screen.fill(BG)
    drawn = set()
    for c, nbrs in city_edges_base.items():
        for n, dist in nbrs.items():
            edge = tuple(sorted([c, n]))
            if edge in drawn: continue
            drawn.add(edge)
            color = ROAD
            width = 8
            if edge in blocked:
                color = ROAD_BLOCKED
                width = 10
            elif len(path) > 1:
                for i in range(len(path)-1):
                    if set(edge) == set([path[i], path[i+1]]):
                        color = ROAD_PATH
                        width = 14
            pygame.draw.line(screen, color, city_positions[c], city_positions[n], width)
            mx = int((city_positions[c][0]+city_positions[n][0])/2)
            my = int((city_positions[c][1]+city_positions[n][1])/2)
            label = small_font.render(str(dist), True, (90,90,90))
            screen.blit(label, (mx-10, my-22))
    for c, pos in city_positions.items():
        color = CITY
        if c in closed_cities:
            color = CITY_CLOSED
        elif c in open_cities:
            color = CITY_EXPLORED
        elif c in selected:
            color = CITY_SELECTED
        pygame.draw.circle(screen, color, pos, CITY_RADIUS)
        pygame.draw.circle(screen, (60,60,60), pos, CITY_RADIUS, 3)
        name = font.render(c, True, (30,30,30))
        screen.blit(name, (pos[0]-CITY_RADIUS, pos[1]-CITY_RADIUS-32))
    txt = "Click two cities: Start then Destination. R = Reset"
    instr = small_font.render(txt, True, (30,30,60))
    screen.blit(instr, (30, HEIGHT-40))
    pygame.display.flip()

def get_city_at_pos(pos):
    for c, p in city_positions.items():
        if math.hypot(pos[0]-p[0], pos[1]-p[1]) < CITY_RADIUS+5:
            return c
    return None

selected = []
path = []
blocked_roads = set()
state = {"open": set(), "closed": set()}
city_edges = apply_traffic(city_edges_base)
running = True

while running:
    draw_map(selected, path, blocked_roads, state["open"], state["closed"])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and len(selected) < 2:
            city = get_city_at_pos(event.pos)
            if city and city not in selected:
                selected.append(city)
                if len(selected) == 2:
                    blocked_roads = get_blocked_roads(city_edges, prob=0.28)
                    state["open"], state["closed"] = set(), set()
                    def draw_callback(cur, open_set, closed_set):
                        state["open"] = set(open_set)
                        state["closed"] = set(closed_set)
                        draw_map(selected, path, blocked_roads, state["open"], state["closed"])
                    start_time = time.time()
                    path = a_star_animated(city_edges, selected[0], selected[1], blocked_roads, draw_callback)
                    duration = time.time() - start_time
                    if path:
                        total_cost = sum(city_edges[path[i]][path[i+1]] for i in range(len(path)-1))
                        print("Path Found:", " -> ".join(path))
                        print("Total Distance:", round(total_cost, 2))
                        print("Computation Time:", round(duration, 3), "seconds")
                        print("Nodes Explored:", len(state["closed"]))
                    else:
                        print("No path found.")
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                selected, path = [], []
                blocked_roads = set()
                state["open"], state["closed"] = set(), set()
                city_edges = apply_traffic(city_edges_base)
    clock.tick(FPS)

pygame.quit()
