from sys import argv

INPUTFILE = "input.txt"
if len(argv) > 1:
    if argv[1] in ("--test", "-t"):
        print("----- TEST MODE -----")
        INPUTFILE = "sample_input.txt"

with open(INPUTFILE) as ifp:
    lines = ifp.read().split("\n")

ranges = []
ingredients = []
for line in lines:
    if "-" in line:
        ranges.append([int(i) for i in line.split("-")])
    elif len(line) == 0:
        continue
    else:
        ingredients.append(int(line))

count = 0
for i in ingredients:
    for r in ranges:
        if i >= r[0] and i <= r[1]:
            count +=1 
            break

print(count)

while True:

    ranges.sort(key = lambda x: x[0])
    new_ranges = []
    for i in range(len(ranges)-1):
        for j in range(i+1, len(ranges)):
            if ranges[i][0] <= ranges[j][0] and ranges[i][1] >= ranges[j][0]:
                new_range = [
                    min([ranges[i][0], ranges[j][0]]),
                    max([ranges[i][1], ranges[j][1]])
                ]
                new_ranges = [ranges[k] for k in range(len(ranges)) if k not in [i, j]]
                new_ranges.append(new_range)
                break

        if new_ranges != []:
            break

    if new_ranges == []: break

    ranges = new_ranges

total = 0
for r in ranges:
    total += ((r[1] - r[0]) + 1)

print(total)



