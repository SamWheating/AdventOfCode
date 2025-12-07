from sys import argv

INPUTFILE = "input.txt"
if len(argv) > 1:
    if argv[1] in ("--test", "-t"):
        print("----- TEST MODE -----")
        INPUTFILE = "sample_input.txt"

with open(INPUTFILE) as ifp:
    lines = ifp.read().split("\n")

splitters = [{x for x in range(len(line)) if line[x] == "^"} for line in lines]

splits = 0
beams = {lines[0].index("S")}
for y in range(1, len(lines)):
    new_beams = set()
    for x in beams:
        if x in splitters[y]:
            new_beams.update({x-1, x+1})
            splits += 1
        else:
            new_beams.add(x)
    beams = new_beams

print(f"part 1: {splits}")

# paths is the number of possible paths which lead to each point
paths = [[0] * len(lines[0]) for y in range(len(lines))]
paths[0][lines[0].index("S")] = 1

# now just iteratively calculate the number of possible ways to pass through given node,
# given the splitters on either side as well as number of paths to the previous level of nodes
for y in range(1, len(paths)):
    for x in range(len(paths[y])):
        if x in splitters[y]:
            # there's no way for a beam to pass through a splitter
            continue
        if x-1 in splitters[y]:
            paths[y][x] += paths[y-1][x-1]
        if x+1 in splitters[y]:
            paths[y][x] += paths[y-1][x+1]
        paths[y][x] += paths[y-1][x]

print(f"part 2: {sum(paths[-1])}")
