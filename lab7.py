import heapq
def is_goal_state(state):
    return state[3] 

def get_next_states(state):
    monkey_at_box, box_at_banana, monkey_on_box, has_banana = state
    next_states = []

    if not monkey_at_box:
        new_state = (True, box_at_banana, monkey_on_box, has_banana)
        next_states.append((1, new_state, "Walk to the box"))

    if monkey_at_box and not box_at_banana:
        new_state = (True, True, monkey_on_box, has_banana)
        next_states.append((1, new_state, "Push the box under the banana"))

    if monkey_at_box and box_at_banana and not monkey_on_box:
        new_state = (monkey_at_box, box_at_banana, True, has_banana)
        next_states.append((1, new_state, "Climb onto the box"))

    if monkey_on_box and box_at_banana and not has_banana:
        new_state = (monkey_at_box, box_at_banana, monkey_on_box, True)
        next_states.append((1, new_state, "Grab the banana"))

    return next_states


def heuristic(state):
    monkey_at_box, box_at_banana, monkey_on_box, has_banana = state
    if has_banana:
        return 0
    
    h = 0
    if not box_at_banana:
        h += 1
    if not monkey_on_box:
        h += 1
    if not has_banana:
        h += 1
    return h

def a_star_search(start_state):
    open_list = [(heuristic(start_state), 0, start_state, [])]
    g_scores = {start_state: 0}
    visited_states = set()

    while open_list:
        f_score, g_score, current_state, path = heapq.heappop(open_list)

        if is_goal_state(current_state):
            return path + [(f"Goal reached! Monkey has the banana!", current_state, g_score)]

        if current_state in visited_states:
            continue
        visited_states.add(current_state)

        for cost, next_state, action in get_next_states(current_state):
            tentative_g_score = g_score + cost
            if tentative_g_score < g_scores.get(next_state, float('inf')):
                g_scores[next_state] = tentative_g_score
                f_score = tentative_g_score + heuristic(next_state)
                new_path = path + [(action, next_state, tentative_g_score)]
                heapq.heappush(open_list, (f_score, tentative_g_score, next_state, new_path))

    return [("No solution found.", None, None)]


if __name__ == "__main__":
    initial_state = (False, False, False, False)

    print("A* Search for the Monkey and Banana Problem\n")
    print(f"Initial State: {initial_state}\n")

    solution_path = a_star_search(initial_state)

    print("--- Solution Path ---")
    for step, state, cost in solution_path:
        if state is not None:
            print(f"Action: {step}\n  New State: {state} | Cost so far: {cost}\n")
        else:
            print(step)
