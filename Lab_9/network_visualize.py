import json
from collections import defaultdict, deque

# Load the JSON dependency graph
with open('django/deps.json') as f:
    deps = json.load(f)

# --- 1. Fan-in / Fan-out Analysis ---
def get_fan_out(deps):
    return {mod: len(submods) for mod, submods in deps.items()}

def get_fan_in(deps):
    fan_in = defaultdict(int)
    for mod, submods in deps.items():
        for submod in submods:
            fan_in[submod] += 1
    return dict(fan_in)

def get_highly_coupled(fan_out, fan_in, top_n=5):
    print("\nTop Coupled Modules by Fan-out:")
    for mod in sorted(fan_out, key=fan_out.get, reverse=True)[:top_n]:
        print(f"{mod}: fan-out = {fan_out[mod]}")
    
    print("\nTop Coupled Modules by Fan-in:")
    for mod in sorted(fan_in, key=fan_in.get, reverse=True)[:top_n]:
        print(f"{mod}: fan-in = {fan_in[mod]}")

# --- 2. Cycle Detection ---
def detect_cycles(deps):
    visited = set()
    stack = set()

    def dfs(node, path):
        if node in stack:
            path.append(node)
            return path
        if node in visited:
            return []
        visited.add(node)
        stack.add(node)
        path.append(node)
        for neighbor in deps.get(node, []):
            result = dfs(neighbor, path.copy())
            if result and node in result:
                return result
        stack.remove(node)
        return []

    found = False
    for node in deps:
        path = dfs(node, [])
        if path:
            cycle_start = path.index(path[-1])
            print("\nCycle Detected:", " -> ".join(path[cycle_start:]))
            found = True
            break
    if not found:
        print("\nNo cycles detected.")

# --- 3. Unused / Disconnected Modules ---
def find_unused_modules(fan_in, fan_out):
    unused = [mod for mod in fan_in if fan_in[mod] == 0]
    disconnected = [mod for mod in unused if fan_out.get(mod, 0) == 0]
    
    print("\nUnused Modules (fan-in = 0):")
    print(unused if unused else "None")
    
    print("\nDisconnected Modules (fan-in = 0 and fan-out = 0):")
    print(disconnected if disconnected else "None")

# --- 4. Dependency Depth ---
def calculate_dependency_depths(deps):
    depths = {}

    def bfs(start):
        visited = set()
        queue = deque([(start, 0)])
        max_depth = 0
        while queue:
            node, depth = queue.popleft()
            visited.add(node)
            max_depth = max(max_depth, depth)
            for neighbor in deps.get(node, []):
                if neighbor not in visited:
                    queue.append((neighbor, depth + 1))
        return max_depth

    for mod in deps:
        depths[mod] = bfs(mod)
    
    print("\nTop 5 Modules by Dependency Depth:")
    for mod, depth in sorted(depths.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"{mod}: depth = {depth}")
# --- 5. Dependencies of Highly Coupled Modules ---
def find_dependencies_of_highly_coupled(fan_out, deps, top_n=5):
    # Get top fan-out modules (highly coupled because they depend on many others)
    top_modules = sorted(fan_out, key=fan_out.get, reverse=True)[:top_n]
    
    print(f"\nTop {top_n} Highly Coupled Modules (by Fan-out) and their Dependencies:")

    for mod in top_modules:
        visited = set()
        queue = deque([mod])
        while queue:
            current = queue.popleft()
            if current not in visited:
                visited.add(current)
                for neighbor in deps.get(current, []):
                    queue.append(neighbor)
        visited.remove(mod)  # exclude self
        print(f"\n{mod} depends on {len(visited)} modules:")
        for dep in sorted(visited):
            print(f"  └── {dep}")

# --- Run all analyses ---
fan_out = get_fan_out(deps)
fan_in = get_fan_in(deps)

get_highly_coupled(fan_out, fan_in)
find_dependencies_of_highly_coupled(fan_out, deps, top_n=5)
detect_cycles(deps)
find_unused_modules(fan_in, fan_out)
calculate_dependency_depths(deps)
