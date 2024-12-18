from sys import argv
from dataclasses import dataclass
from typing import List, Dict, Set, Tuple, Any, Optional
from enum import Enum
import re
from collections import defaultdict


class Op(Enum):
    ADV = 0 # division: A / 2^combo(arg) -> A
    BXL = 1 # bitwise xor: B ^ lit(arg) -> B
    BST = 2 # combo(arg) % 8 -> B
    JNZ = 3 # jump nonzero: if A != 0: goto lit(arg)
    BXC = 4 # bitwise xor: B ^ C -> B
    OUT = 5 # combo(arg) % 8 -> stdout
    BDV = 6 # division: A / 2^combo(arg) -> B
    CDV = 7 # division: A / 2^combo(arg) -> C

class Instruction:

    def __init__(self, opcode: int, arg: int) -> None:
        self.op: Op = Op(opcode)
        self.arg: int = arg

class Computer:

    def __init__(self, r_a: int, r_b: int, r_c: int, prog: List[int]):
        self.a: int = r_a
        self.b: int = r_b
        self.c: int = r_c
        self.ip: int = 0
        self.prog: List[int] = prog
        self.cache: Dict[str, str] = {} # cache of state to final stdout

    def __repr__(self) -> str:
        return f"A: {self.a}, B: {self.b}, C: {self.c}, IP: {self.ip}"
    
    def resolve_combo_operand(self, op: int) -> int:
        if op <= 3 and op >= 0:
            return op
        elif op == 4: return self.a
        elif op == 5: return self.b
        elif op == 6: return self.c
        raise Exception(f"Invalid combo operand {op}")

    def step(self) -> Optional[str]:
        
        inst = Instruction(self.prog[self.ip], self.prog[self.ip + 1])
        retval = None
        
        # first resolve the operand. Some opcodes use combo format:
        if inst.op in {Op.ADV, Op.BST, Op.OUT, Op.BDV, Op.CDV}:
            arg = self.resolve_combo_operand(inst.arg)
        else:
            arg = inst.arg

        # now run the instruction
        if inst.op == Op.ADV:
            self.a = self.a // (2**arg)
        
        elif inst.op == Op.BXL:
            self.b ^= arg

        elif inst.op == Op.BST:
            self.b = arg % 8
            
        elif inst.op == Op.JNZ:
            if self.a != 0:
                self.ip = arg - 2 # this corrects for the +2 after every instruction
        
        elif inst.op == Op.BXC:
            self.b = self.b ^ self.c

        elif inst.op == Op.OUT:
            retval = arg % 8
        
        elif inst.op == Op.BDV:
            self.b = self.a // (2**arg)

        elif inst.op == Op.CDV:
            self.c = self.a // (2**arg)

        self.ip += 2
        return retval

    @property
    def statehash(self) -> int:
        return hash((self.a, self.b, self.c, self.ip))

    def run(self) -> List[int]:
        # run the program until it halts, then return a comma-separated list of outputs
        # additionally, if we are in a previously-seen state, early return the eventual stdout
        output = []
        states: Dict[int, List[int]] = {} # map of states to eventual outputs

        while True:
            
            # maybe we're done?
            if self.ip >= len(self.prog):
                for s in states:
                    self.cache[s] = states[s]
                return output

            # maybe we've seen this state before?
            if self.statehash in self.cache:
                remainder = self.cache[self.statehash]
                for s in states:
                    states[s].extend(remainder)
                    self.cache[s] = states[s]
                return output + remainder
            
            # brand new state!
            states[self.statehash] = []
            
            v = self.step()
            if v is not None:
                output.append(v)
                for s in states:
                    states[s].append(v)

c = Computer(0,0,9, [2,6])
c.step()
assert c.b == 1

c = Computer(10,10,0, [5,0,5,1,5,4])
assert c.run() == [0,1,2]

def part1(a,b,c,prog):
    computer = Computer(a, b, c, prog)
    stdout = computer.run()
    return ",".join([str(i) for i in stdout])

def part2(b,c,prog):
    computer = Computer(0, b, c, prog)
    new_a = 0
    while True:
        # reset state of computer
        computer.a = new_a
        computer.b = b
        computer.c = c
        computer.ip = 0

        stdout = computer.run()
        if stdout == prog:
            return new_a
        
        new_a += 1

if __name__ == "__main__":

    INPUTFILE = "input.txt"
    if len(argv) > 1:
        if argv[1] in ("--test", "-t"):
            print("----- TEST MODE -----")
            INPUTFILE = "sample_input.txt"

    with open(INPUTFILE) as ifile:
        lines = ifile.read().splitlines()

    a = int(lines[0].split(" ")[2])
    b = int(lines[1].split(" ")[2])
    c = int(lines[2].split(" ")[2])
    prog = [int(i) for i in lines[4].split(" ")[1].split(",")]
    computer = Computer(a, b, c, prog)

    print(f"Part 1: {part1(a,b,c,prog)}")
    print(f"Part 2: {part2(b,c,prog)}")
