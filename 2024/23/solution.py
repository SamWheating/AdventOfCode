from sys import argv
from dataclasses import dataclass
from typing import List, Dict, Set, Tuple, Any
import re
from collections import defaultdict

def part1(conns: Set[Set[str]]):

    # TODO: learn a less crappy alg for connected components in an undirected graph
    # (this is off the top of my head)
    
    nodes = set()
    for c in conns:
        nodes |= c
    nodes = list(nodes)

    groups: Set[str] = set()
    for i in range(len(nodes)-2):
        for j in range(i+1, len(nodes)-1):
            if frozenset({nodes[i], nodes[j]}) not in conns:
                continue
            for k in range(i+2, len(nodes)):
                if frozenset({nodes[i], nodes[k]}) not in conns:
                    continue
                if frozenset({nodes[j], nodes[k]}) not in conns:
                    continue
                groups.add(frozenset({nodes[i], nodes[j], nodes[k]}))

    total = 0
    for g in groups:
        for n in g:
            if n[0] == "t":
                total += 1
                break

    return total

def part2(conns: Set[Set[str]]):

    nodes = set()
    for c in conns:
        nodes |= c
    nodes = list(nodes)

    components: Set[Set[str]] = set([frozenset({n}) for n in nodes])
    while True:
        new_components: Set[Set[str]] = set()
        for component in components:
            for n1 in nodes:
                for n2 in component:
                    if n1 == n2:
                        break
                    if n1 in component:
                        break
                    if {n1, n2} not in conns:
                        break
                else:
                    new_components.add(component.union({n1}))
        
        if len(new_components) == 0:
            break
        
        components = new_components

    assert len(components) == 1

    return ",".join(sorted(list(components)[0]))

if __name__ == "__main__":

    INPUTFILE = "input.txt"
    if len(argv) > 1:
        if argv[1] in ("--test", "-t"):
            print("----- TEST MODE -----")
            INPUTFILE = "sample_input.txt"

    conns: Set[Set[str]] = set()
    with open(INPUTFILE) as ifile:
        for line in ifile.read().splitlines():
            conn = frozenset({
                line.split("-")[0],
                line.split("-")[1]
            })
            conns.add(conn)
    
    print(f"Part 1: {part1(conns)}")
    print(f"Part 2: {part2(conns)}")
