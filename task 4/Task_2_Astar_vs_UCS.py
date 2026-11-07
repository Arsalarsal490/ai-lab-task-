import heapq

# Campus graph: each edge is (neighbor, cost)
graph = {
    "S": [("A", 1), ("B", 4)],
    "A": [("C", 2)],
    "B": [("G", 5)],
    "C": [("G", 3)],
    "G": []
}

heuristic = {"S": 5, "A": 4, "B": 4, "C": 2, "G": 0}


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


def ucs(graph, start, goal):
    """Uniform Cost Search is A* with h(n) = 0 for every node."""
    zero_h = {node: 0 for node in graph}
    return astar(graph, zero_h, start, goal)


def verify_path_cost(graph, path):
    """Independently sum the edge weights along a returned path."""
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
    print("TASK 2: A* versus UCS")
    print_result("A* with supplied heuristic", astar(graph, heuristic, "S", "G"))
    print_result("UCS (zero heuristic)", ucs(graph, "S", "G"))
    print("Counting convention: a non-goal node counts as an expansion")
    print("when its successors are processed. The goal is popped but not expanded.")
