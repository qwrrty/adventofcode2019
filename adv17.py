#! /usr/bin/env python3

from intcode import Intcode

class ASCIIRobot(object):

    def __init__(self):
        self.intcode = Intcode.from_file("adv17_input.txt")
        self.scaffold_map = []
        self.height = 0
        self.width = 0

    def map_area(self):
        self.intcode.run()
        self.scaffold_map = []
        row = ""
        for o in self.intcode.outputs:
            char = chr(o)
            if char == "\n":
                self.scaffold_map.append(row)
                row = ""
            else:
                row += char
        while not self.scaffold_map[-1]:
            self.scaffold_map.pop()

        self.height = len(self.scaffold_map)
        self.width = len(self.scaffold_map[0])


def part1():
    robot = ASCIIRobot()
    robot.map_area()
    
    alignment_params = 0
    for y, row in enumerate(robot.scaffold_map):
        if not row:
            continue
        for x, ch in enumerate(row):
            if ch != "#":
                continue
            if ((y == 0 or robot.scaffold_map[y-1][x] == "#") and
                (y == robot.height-1 or robot.scaffold_map[y+1][x] == "#") and
                (x == 0 or robot.scaffold_map[y][x-1] == "#") and
                (x == robot.width-1 or robot.scaffold_map[y][x+1] == "#")):
                alignment_params += x * y

    print(alignment_params)
