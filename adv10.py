#! /usr/bin/env python3

import math

from collections import defaultdict

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
                if rows[y][x] != ".":
                    self.grid[Point(x,y)] = True
        self.height = len(rows)
        self.width = len(rows[0])

    def render(self):
        rows = []
        for y in range(0, self.height):
            row = ["#" if Point(x,y) in self.grid else "." for x in range(0, self.width)]
            rows.append("".join(row))
        return "\n".join(rows)

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

        if xdelta == 0 and ydelta == 0:
            return []

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

    def vaporize_asteroids(self, station, limit=200):
        # With a laser cannon mounted at the Point defined by station,
        # sweep around the map vaporizing asteroids. Stop when vaporized
        # asteroids exceed the given limit, or when all asteroids (except
        # station) have been vaporized. Return the list of vaporized asteroids
        # in order of destruction.
        #
        # To determine the order in which to vaporize asteroids:
        #
        # 1. Measure the angle from the Y-axis to each asteroid.
        # 2. Build a mapping from angles to a list of asteroids found along
        #    that angle.
        # 3. Sort each sub-list of asteroids by distance from station.
        # 4. Iterate through the mapping in numerical order by angle, popping
        #    one asteroid off each list as we go.
        #
        # Notes:
        #
        # Calculating the angle between the target asteroid and the y-axis
        # is easier if we calculate it as atan(x_delta, y_delta) rather than
        # atan(y_delta, x_delta). Doing so makes the vertical Y axis start at -pi
        # radians and increase as we sweep clockwise through the field, which is
        # what we want for sorting purposes.

        def distance(p):
            return math.sqrt((p.x-station.x)**2 + (p.y-station.y)**2)
        
        # Map angles to asteroids.
        angles = defaultdict(list)
        for p in self.grid:
            if p == station:
                continue
            rad = math.atan2(p.x-station.x, p.y-station.y)
            angles[rad].append(p)

        # Sort each bucket by distance from the station
        for rad in angles:
            angles[rad].sort(key=distance)

        # Now walk through the map in order of angle and pop off asteroids one by one
        vaporized = []
        while angles and len(vaporized) < limit:
            for rad in sorted(angles.keys(), reverse=True):
                vaporized.append(angles[rad].pop(0))
                if len(vaporized) >= limit:
                    break
            # Remove any empty lists
            empty = [rad for rad in angles if not angles[rad]]
            for rad in empty:
                del angles[rad]

        return vaporized


def part1():
    m = AsteroidMap.from_file("adv10_input.txt")
    station, count = m.find_best_station()
    print(station, count)

def part2():
    m = AsteroidMap.from_file("adv10_input.txt")
    station, count = m.find_best_station()
    vaporized = m.vaporize_asteroids(station, limit=200)
    a = vaporized[-1]
    print(a.x * 100 + a.y)
