from sys import argv

def part1(lines):
    l, r = [], []
    for line in lines:
        l.append(int(line.split()[0]))
        r.append(int(line.split()[1]))
    
    l.sort()
    r.sort()

    dist = 0
    for i in range(len(l)):
        dist += abs(l[i] - r[i])
    return dist

assert part1(["1 0", "3 0"]) == 4

def part2(lines):
    l, r = [], []
    for line in lines:
        l.append(int(line.split()[0]))
        r.append(int(line.split()[1]))

    score = 0
    for i in range(len(l)):
        score += l[i] * r.count(l[i])
    return score

assert part2(["1 1", "3 1", "2 3"]) == 5

if __name__ == "__main__":

    INPUTFILE = "input.txt"
    if len(argv) > 1:
        if argv[1] in ("--test", "-t"):
            print("----- TEST MODE -----")
            INPUTFILE = "sample_input.txt"

    with open(INPUTFILE) as ifile:
        contents = ifile.read()
        lines = contents.splitlines()

    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
