#! /usr/bin/env python3

import math


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "<Point ({},{})>".format(self.x, self.y)

    def __eq__(self, p):
        return self.x == p.x and self.y == p.y

    def __hash__(self):
        return (self.x, self.y).__hash__()

class AsteroidMap(object):

    def __init__(self, data):
        self.grid = dict()
        rows = data.split()
        for y in range(0, len(rows)):
            for x in range(0, len(rows[y])):
                if rows[y][x] == "#":
                    self.grid[Point(x,y)] = True

    def from_file(filename):
        with open(filename, "r") as f:
            data = f.read().strip()
        return AsteroidMap(data)

    def lookup(self, p):
        return self.grid.get(p, False)

    def points_between(self, p1, p2):
        # Return a list of Points that lie on the map between p1 and p2
        # (excluding endpoints).
        # Points are returned in order starting from p1.

        # The tricky part is to identify which points on the line segment
        # between (x1,y1) and (x2,y2) are also on the grid, i.e. have integral
        # coordinates. We find the slope between the two target points expressed
        # as the y-delta and x-delta. Then divide both deltas by their greatest
        # common divisor. The result is the smallest integral slope between the
        # two points. We then can find all of the integral coordinates that
        # lie on the line segment by starting at (x1,y1) and repeatedly adding
        # the minimal x and y deltas.
        
        ydelta = p2.y - p1.y
        xdelta = p2.x - p1.x

        gcd = math.gcd(xdelta, ydelta)
        ydelta //= gcd
        xdelta //= gcd

        points = []
        x = p1.x + xdelta
        y = p1.y + ydelta
        while Point(x,y) != p2:
            points.append(Point(x,y))
            x += xdelta
            y += ydelta
        return points
    
    def count_visible_asteroids(self, p0):
        # Count asteroids in direct line of sight from p0.
        visible_asteroids = {}
        for p in self.grid:
            if p == p0:
                continue
            # Find the first asteroid on the line between p0 and p
            midpoints = self.points_between(p0, p)
            for q in midpoints:
                if self.lookup(q):
                    visible_asteroids[q] = True
                    break
            else:
                # No asteroids found along the line, so add p
                visible_asteroids[p] = True
                
        return len(visible_asteroids.keys())
    
    def find_best_station(self):
        counts = {}
        for p in self.grid:
            counts[p] = self.count_visible_asteroids(p)
        station = max(counts, key=counts.get)
        return station, counts[station]
        
def part1():
    m = AsteroidMap.from_file("adv10_input.txt")
    station, count = m.find_best_station()
    print(station, count)
