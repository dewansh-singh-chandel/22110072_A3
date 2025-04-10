import json
from collections import defaultdict

with open('django/deps.json') as f:
    data = json.load(f)

fan_out = {mod: len(deps) for mod, deps in data.items()}
fan_in = defaultdict(int)

for mod, deps in data.items():
    for dep in deps:
        fan_in[dep] += 1

print("Fan-out:", fan_out)
print("Fan-in:", dict(fan_in))
