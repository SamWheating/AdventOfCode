from collections import defaultdict

from sys import argv
from typing import List

INPUTFILE = "input.txt"

if len(argv) > 1:
    if argv[1] in ("--test", "-t"):
        print("----- TEST MODE -----")
        INPUTFILE = "sample_input.txt"

with open(INPUTFILE) as ifp:
    lines = ifp.read().split("\n")

nodes = defaultdict(list)
for line in lines:
    nodes[line[:3]] = line[5:].split()

def count_paths_between(nodes, start, end):

    num_paths = defaultdict(int)
    num_paths[start] = 1

    total_paths = 0
    while True:
        new_num_paths = defaultdict(int)
        for parent, paths in num_paths.items():
            if paths == 0:
                continue
            for child in nodes[parent]:
                if child == end:
                    total_paths += paths
                new_num_paths[child] += paths
        
        num_paths = new_num_paths

        if sum(num_paths.values()) == 0:
            return total_paths

print(f"part 1: {count_paths_between(nodes, 'you', 'out')}")

# to find paths between SVR and OUT which pass through DAC and FFT, we need to look at two possible paths:
#
#  SVR -> DAC -> FFT -> OUT
#  SVR -> FFT -> DAC -> OUT
#
# We can just find the number of paths between any two nodes in these sequences, and then multiply them
# in order to get the total number of paths.
#
# This assumes that there's no loops, since that would result in an infinite number of solutions.

paths_svr_to_dac = count_paths_between(nodes, "svr", "dac")
paths_dac_to_fft = count_paths_between(nodes, "dac", "fft")
paths_fft_to_out = count_paths_between(nodes, "fft", "out")

paths_svr_to_fft = count_paths_between(nodes, "svr", "fft")
paths_fft_to_dac = count_paths_between(nodes, "fft", "dac")
paths_dac_to_out = count_paths_between(nodes, "dac", "out")

part2 = (paths_svr_to_dac * paths_dac_to_fft * paths_fft_to_out) + (paths_svr_to_fft * paths_fft_to_dac * paths_dac_to_out)

print(f"part 2: {part2}")
