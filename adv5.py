#! /usr/bin/env python3

from intcode import Intcode


def part1(data):
    intcode = Intcode(data)
    intcode.run()
    print(intcode.outputs)
    
def read_input(filename):
    data = []
    with open(filename, "r") as f:
        for line in f:
            data.extend([int(x) for x in line.split(",")])
    return data


if __name__ == "__main__":
    data = read_input("adv5_input.txt")
    part1(data)
