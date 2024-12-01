# This is the boilerplate I usually start with
from sys import argv

def part1(lines):
    pass

def part2(lines):
    pass

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
