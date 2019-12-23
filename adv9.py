#! /usr/bin/env python3

from intcode import Intcode

def part1(filename="adv9_input.txt"):
    intcode = Intcode.from_file(filename, inputs=[1])
    intcode.run()
    print(intcode.outputs)

def part2(filename="adv9_input.txt"):
    intcode = Intcode.from_file(filename, inputs=[2])
    intcode.run()
    print(intcode.outputs)
    
if __name__ == "__main__":
    part1()
