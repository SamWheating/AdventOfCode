# This is the boilerplate I usually start with
from sys import argv

def part1(lines):
    found = 0
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == "X":
                # Wow I super hate this, but I am trying to be speedy here.
                # forwards:
                if x < len(lines[y]) - 3:
                    if lines[y][x] + lines[y][x+1] + lines[y][x+2] + lines[y][x+3] == "XMAS":
                        found += 1

                # backwards
                if x >= 3:
                    if lines[y][x] + lines[y][x-1] + lines[y][x-2] + lines[y][x-3] == "XMAS":
                        found += 1

                # upwards
                if y >= 3:
                    if lines[y][x] + lines[y-1][x] + lines[y-2][x] + lines[y-3][x] == "XMAS":
                        found += 1

                # downwards
                if y < len(lines)-3:
                    if lines[y][x] + lines[y+1][x] + lines[y+2][x] + lines[y+3][x] == "XMAS":
                        found += 1

                # up + left
                if x >= 3 and y >= 3:
                    if lines[y][x] + lines[y-1][x-1] + lines[y-2][x-2] + lines[y-3][x-3] == "XMAS":
                        found += 1

                # up + right
                if x < len(lines[y]) - 3 and y >= 3:
                    if lines[y][x] + lines[y-1][x+1] + lines[y-2][x+2] + lines[y-3][x+3] == "XMAS":
                        found += 1

                # down + left
                if x >= 3 and y < len(lines)-3:
                    if lines[y][x] + lines[y+1][x-1] + lines[y+2][x-2] + lines[y+3][x-3] == "XMAS":
                        found += 1

                # down + right
                if x < len(lines[y]) - 3 and y < len(lines)-3:
                    if lines[y][x] + lines[y+1][x+1] + lines[y+2][x+2] + lines[y+3][x+3] == "XMAS":
                        found += 1

    return found


assert part1([
    "XMASX",
    "SAMXM",
    "BLASA",
    "BLAHS"
]) ==  3

def part2(lines):

    found = 0
    for y in range(1,len(lines)-1):
        for x in range(1, len(lines[y])-1):
            if lines[y][x] == "A": # look for centers
                if sorted([
                    lines[y-1][x-1],
                    lines[y-1][x+1],
                    lines[y+1][x-1],
                    lines[y+1][x+1],
                ]) == ["M","M","S","S"]:
                    if lines[y-1][x-1] != lines[y+1][x+1]:
                        found += 1

    return found

assert part2([
    "M.S.M",
    ".A.A.",
    "M.S.M"
]) ==  2

if __name__ == "__main__":

    INPUTFILE = "input.txt"
    if len(argv) > 1:
        if argv[1] in ("--test", "-t"):
            print("----- TEST MODE -----")
            INPUTFILE = "sample_input.txt"

    with open(INPUTFILE) as ifile:
        lines = ifile.readlines()
        line = ifile.read()

    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
