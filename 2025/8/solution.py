from sys import argv
from math import sqrt

INPUTFILE = "input.txt"
N_CIRCUITS = 1000

if len(argv) > 1:
    if argv[1] in ("--test", "-t"):
        print("----- TEST MODE -----")
        INPUTFILE = "sample_input.txt"
        N_CIRCUITS = 10

with open(INPUTFILE) as ifp:
    lines = ifp.read().split("\n")

class Node():

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def dist(self, other: "Node") -> float:
        return sqrt(
            (self.x - other.x) ** 2 +
            (self.y - other.y) ** 2 +
            (self.z - other.z) ** 2
        )

    def __repr__(self):
        return f"({self.x},{self.y},{self.z})"

nodes = {}
for n in range(len(lines)):
    x, y, z = (int(i) for i in lines[n].split(","))
    nodes[n] = Node(x,y,z)

# list of pairing + distance tuples
pairings = []

# find the distance between all pairs of nodes, sort ascending
for a in range(len(nodes)-1):
    for b in range(a, len(nodes)):
        if a == b: continue
        pairings.append((a, b, nodes[a].dist(nodes[b])))

pairings.sort(key = lambda x: x[2])
shortest = pairings[:N_CIRCUITS]

# now create connected components
components = {frozenset([i]) for i in nodes}
for connection in shortest:
    components.add(frozenset([connection[0], connection[1]]))

# now just brute-force reduce the connected components:
# this could be wayyy faster, but still runs in ~10s
while True:
    new_components = {c for c in components}
    size = len(components)
    for a in components:
        for b in components:
            if a & b and a != b:
                new_components.remove(a)
                new_components.remove(b)
                new_components.add(frozenset(a | b))
                break
        if len(new_components) != len(components):
            break
    else:
        break

    components = new_components

sizes = [len(c) for c in components]
sizes.sort()

print(f"part 1: {sizes[-3] * sizes[-2] * sizes[-1]}")

# part 2: just scan down the list of shortest connections until we've seen every node
unseen = {k for k in nodes.keys()}
for p in pairings:
    a, b, _  = p
    unseen.discard(a)
    unseen.discard(b)
    if len(unseen) == 0:
        break

print(f"part 2: {nodes[a].x * nodes[b].x}")
