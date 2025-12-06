from functools import reduce
from sys import argv

INPUTFILE = "input.txt"
if len(argv) > 1:
    if argv[1] in ("--test", "-t"):
        print("----- TEST MODE -----")
        INPUTFILE = "sample_input.txt"

with open(INPUTFILE) as ifp:
    lines = ifp.read().split("\n")

operands = []
for line in lines[:-1]:
    operands.append([int(i) for i in line.split()])

operators = lines[-1].split()

funcs = {
    "+": lambda x, y: x+y,
    "*": lambda x, y: x*y
}

total = 0
for i in range(len(operators)):
    op = operators[i]
    args = [o[i] for o in operands]

    total += reduce(funcs[op], args)

print(f"part 1: {total}")

# part 2
idx = 0
total = 0

vals = []
while True:

    if idx == len(lines[0]):
        total += reduce(funcs[op], vals)
        print(f"part 2: {total}")
        break

    if lines[-1][idx] != " ":
        op = lines[-1][idx]
    
    chars = [lines[i][idx] for i in range(len(lines)-1)]
    if all([c == " " for c in chars]):
        total += reduce(funcs[op], vals)
        vals = []

    else:
        vals.append(int("".join([c for c in chars if c != " "])))

    idx += 1