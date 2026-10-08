# AI Lab 3: Depth-Limited Search (DLS) and Iterative Deepening DFS (IDDFS)
# Original graph, with children explored in the listed order:
# A: B, C
# B: D, E
# C: F
# D, E, F, G: no children
# Start = A, Goal = G. Root A is at depth 0.

graph = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F"],
    "D": [],
    "E": ["G"],
    "F": [],
    "G": [],
}
START = "A"
GOAL = "G"


def dls(node, limit, path):
    # Goal test first, so a goal at the boundary counts as FOUND.
    if node == GOAL:
        return "FOUND", path

    # Reached the depth limit before finding the goal.
    if len(path) - 1 == limit:
        return "CUTOFF", None

    saw_cutoff = False
    for child in graph[node]:
        # Path-local cycle check; no global visited set is used.
        if child in path:
            continue

        status, found_path = dls(child, limit, path + [child])
        if status == "FOUND":
            return "FOUND", found_path
        if status == "CUTOFF":
            saw_cutoff = True

    if saw_cutoff:
        return "CUTOFF", None
    return "FAILURE", None


def show_path(path):
    return " -> ".join(path) if path else "None"


print("GRAPH: A:[B,C], B:[D,E], C:[F], E:[G]; start=A, goal=G")
print("Root depth = 0; child order is left-to-right.")
print("\nDLS RESULTS")
for limit in [1, 2, 3, 4]:
    status, path = dls(START, limit, [START])
    print(f"Limit {limit}: status={status}; path={show_path(path)}")

print("\nIDDFS RESULTS")
for max_depth in [1, 2, 3, 4]:
    attempted = []
    final_status, final_path = "CUTOFF", None

    for limit in range(0, max_depth + 1):
        attempted.append(limit)
        status, path = dls(START, limit, [START])
        final_status, final_path = status, path
        if status == "FOUND" or status == "FAILURE":
            break

    print(
        f"Maximum depth {max_depth}: status={final_status}; "
        f"path={show_path(final_path)}; limits attempted={attempted}"
    )

print("\nINTERPRETATION")
print("Limits below 3 cannot reach G because the path A -> B -> E -> G has goal depth 3.")
print("IDDFS repeats shallow exploration at each new limit, trading extra work for low memory use.")
