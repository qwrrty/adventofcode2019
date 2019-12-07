#! /usr/bin/env python3

from collections import defaultdict


class Point(object):

    # A Point represents a point on the Cartesian plane. We will use these
    # to keep track of which points in a WirePanel have wires going
    # through them.
    #
    # The advantage of this representation is that a Point's hash is
    # defined to guarantee that two Points with the same coordinates
    # will hash to the same value -- making it easy to tell quickly
    # if a point is occupied in the panel -- and the x and y values
    # are accessible as properties, making it easy to calculate
    # Manhattan distances between points.
    #
    # For simplicity of hashing we assume that the point space is
    # no more than 10,000 points on a side.
    
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def __eq__(self, other):
        return self._x == other.x and self._y == other.y

    def __hash__(self):
        # Return a consistent hash value for points with identical coords
        return self._y * 10000 + self._x

    def __repr__(self):
        return "<Point [{},{}]>".format(self._x, self._y)
    
    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @x.setter
    def x(self, value):
        self._x = value

    @y.setter
    def y(self, value):
        self._y = value


class WirePanel(object):

    # A WirePanel object represents the state of a wire panel
    # and which intersections have been crossed.
    #
    # The wire_points member is a dict that describes which points
    # are crossed by a wire.
    # Each key of this dict is a Point.
    # Each value is another dict, listing the wires that pass through
    # that point and how many steps it takes each one to get there.
    #
    # Example:
    #
    # Point(3,7): {"A": 10}
    # Point(4,7): {"A": 11}
    # Point(5,7): {"A": 12, "B": 17}
    #
    # The "central port" is defined as 0,0.
    
    def __init__(self):
        self.wire_points = defaultdict(dict)

    def point(self, x, y):
        return self.wire_points[Point(x,y)]

    def add_wire(self, wire, label):
        # The "wire" argument is a string describing a wire's shape,
        # e.g. "R8,U5,L5,D3"

        x = 0
        y = 0
        steps = 0
        segments = wire.split(",")
        for s in segments:
            if s.startswith("R"):
                ix = 1
                iy = 0
            elif s.startswith("L"):
                ix = -1
                iy = 0
            elif s.startswith("U"):
                ix = 0
                iy = 1
            elif s.startswith("D"):
                ix = 0
                iy = -1
            else:
                raise Exception("unknown direction {}".format(s))

            seg_length = int(s[1:])
            for n in range(0, seg_length):
                x += ix
                y += iy
                steps += 1
                current_wires = self.point(x,y)
                if label not in current_wires:
                    current_wires[label] = steps

    def intersections(self):
        return [p for p, wires in self.wire_points.items() if len(wires) > 1]


def read_input(filename):
    with open(filename, "r") as f:
        return f.readlines()

    
def part1(panel):
    # Find the intersection with the lowest Manhattan distance
    return min(abs(p.x) + abs(p.y) for p in panel.intersections())


def part2(panel):
    return min(sum(panel.point(p.x, p.y).values()) for p in panel.intersections())

if __name__ == "__main__":
    panel = WirePanel()
    label = 0
    wires = read_input("adv3_input.txt")
    for w in wires:
        panel.add_wire(w, label)
        label += 1
    result = part2(panel)
    print(result)

