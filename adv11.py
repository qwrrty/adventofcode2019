#! /usr/bin/env python3

from intcode import Intcode

from collections import defaultdict

BLACK = 0
WHITE = 1

TURN_LEFT = 0
TURN_RIGHT = 1

# Directions are ordered so that TURN_RIGHT can be executed
# with current_dir + 1 % 4, and TURN_LEFT can be executed
# with current_dir - 1 % 4

DIR_UP = 0
DIR_RIGHT = 1
DIR_DOWN = 2
DIR_LEFT = 3

class Panel(object):
    
    def __init__(self, color=BLACK):
        self.color = color
        self.robot_painted = False

class Robot(object):

    def __init__(self):
        self.panels = defaultdict(Panel)
        self.intcode = Intcode.from_file("adv11_input.txt")
        self.x = 0
        self.y = 0
        self.direction = DIR_UP

    def render(self):
        # Find the boundaries of the map
        min_x = min(point[0] for point in self.panels)
        max_x = max(point[0] for point in self.panels)
        min_y = min(point[1] for point in self.panels)
        max_y = max(point[1] for point in self.panels)

        rows = []
        for y in range(min_y, max_y+1):
            rows.append("".join(
                ["#" if self.panels[(x,y)].color == WHITE else "."
                 for x in range(min_x, max_x+1)]))
        return "\n".join(rows)
            
    def current_panel(self):
        return self.panels[(self.x,self.y)]
    
    def current_color(self):
        return self.current_panel().color
    
    def paint(self, new_color):
        p = self.current_panel()
        p.color = new_color
        p.robot_painted = True

    def turn(self, direction):
        self.direction += 1 if direction == TURN_RIGHT else -1
        self.direction %= 4

    def move_forward(self):
        if self.direction == DIR_UP:
            self.y -= 1
        elif self.direction == DIR_DOWN:
            self.y += 1
        elif self.direction == DIR_LEFT:
            self.x -= 1
        elif self.direction == DIR_RIGHT:
            self.x += 1
        else:
            raise Exception("unknown direction {}".format(self.direction))
            
    def run(self):
        while True:
            self.intcode.add_input(self.current_color())
            new_color = self.intcode.run(break_on_output=True)
            if new_color is None:
                # Intcode has halted
                return
            direction = self.intcode.run(break_on_output=True)
            self.paint(new_color)
            self.turn(direction)
            self.move_forward()

def part1():
    r = Robot()
    r.run()
    print(sum(1 for p, panel in r.panels.items() if panel.robot_painted))

def part2():
    r = Robot()
    r.current_panel().color = WHITE
    r.run()
    print(r.render())
