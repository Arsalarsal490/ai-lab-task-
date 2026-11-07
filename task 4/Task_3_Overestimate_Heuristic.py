import heapq

# Campus graph: each edge is (neighbor, cost)
graph = {
    "S": [("A", 1), ("B", 4)],
    "A": [("C", 2)],
    "B": [("G", 5)],
    "C": [("G", 3)],
    "G": []
}

original_heuristic = {"S": 5, "A": 4, "B": 4, "C": 2, "G": 0}
modified_heuristic = {**original_heuristic, "C": 10}  # Change only h(C)


def astar(graph, h, start, goal):
    """Return (path_cost, path, popped_trace, expansion_count)."""
    pq = [(h[start], 0, start, [start])]
    best = {start: 0}
    popped_trace = []
    expansions = 0

    while pq:
        f, g_cost, node, path = heapq.heappop(pq)
        popped_trace.append((node, g_cost, f))

        # Match the supplied implementation: goal check before stale check.
        if node == goal:
            return g_cost, path, popped_trace, expansions

        if g_cost != best[node]:
            continue

        expansions += 1
        for nxt, weight in graph.get(node, []):
            new_cost = g_cost + weight
            if new_cost < best.get(nxt, float("inf")):
                best[nxt] = new_cost
                heapq.heappush(
                    pq,
                    (new_cost + h[nxt], new_cost, nxt, path + [nxt])
                )

    return None, [], popped_trace, expansions


def true_remaining_cost(graph, start, goal):
    """Use UCS to find the true minimum cost from start to goal."""
    pq = [(0, start)]
    best = {start: 0}
    while pq:
        cost, node = heapq.heappop(pq)
        if cost != best[node]:
            continue
        if node == goal:
            return cost
        for nxt, weight in graph.get(node, []):
            new_cost = cost + weight
            if new_cost < best.get(nxt, float("inf")):
                best[nxt] = new_cost
                heapq.heappush(pq, (new_cost, nxt))
    return float("inf")


def verify_path_cost(graph, path):
    total = 0
    for current, nxt in zip(path, path[1:]):
        for neighbor, weight in graph[current]:
            if neighbor == nxt:
                total += weight
                break
        else:
            raise ValueError(f"No edge found from {current} to {nxt}")
    return total


def print_result(label, result):
    cost, path, trace, expansions = result
    print(f"--- {label} ---")
    print("Returned path:", " -> ".join(path))
    print("Returned cost:", cost)
    print("Independently summed path cost:", verify_path_cost(graph, path))
    print("Popped/processed trace (node, g, priority):")
    for item in trace:
        print(" ", item)
    print("Non-goal expansion count:", expansions)
    print("Popped count including goal:", len(trace))
    print()


if __name__ == "__main__":
    true_cost_from_c = true_remaining_cost(graph, "C", "G")
    print("TASK 3: Overestimate experiment")
    print(f"True remaining cost h*(C): {true_cost_from_c}")
    print(f"Original h(C): {original_heuristic['C']}")
    print(f"Modified h(C): {modified_heuristic['C']}")
    print(f"Modified overestimate amount: {modified_heuristic['C'] - true_cost_from_c}")
    print("Only h(C) is changed; graph and all other heuristic values stay the same.")
    print()

    print_result(
        "Original heuristic",
        astar(graph, original_heuristic, "S", "G")
    )
    print_result(
        "Modified heuristic with h(C) = 10",
        astar(graph, modified_heuristic, "S", "G")
    )
