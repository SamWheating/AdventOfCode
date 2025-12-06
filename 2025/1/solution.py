from sys import argv

INPUTFILE = "input.txt"
if len(argv) > 1:
    if argv[1] in ("--test", "-t"):
        print("----- TEST MODE -----")
        INPUTFILE = "sample_input.txt"

with open(INPUTFILE) as ifp:
    lines = ifp.readlines()

count_1 = 0
count_2 = 0
pos = 50
for line in lines:

    init_pos = pos

    d = 1 if line[0] == "R" else -1
    mag = int(line[1:])

    count_2 += abs(mag) // 100
    mag %= 100

    pos += (mag * d)
    if pos > 100:
        count_2 += 1

    if pos < 0 and init_pos != 0:
        count_2 += 1 

    pos %= 100

    if pos == 0:
        count_1 += 1
        count_2 += 1

print(f"Part 1 solution: {count_1}")
print(f"Part 2 solution: {count_2}")