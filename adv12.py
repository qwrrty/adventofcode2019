#! /usr/bin/env python3

import itertools
import re


class Moon(object):

    def __init__(self, x, y, z):
        self.pos = [x, y, z]
        self.vel = [0, 0, 0]

    def __repr__(self):
        return "<Moon pos={} vel={}>".format(self.pos, self.vel)

    def potential_energy(self):
        return sum(abs(x) for x in self.pos)

    def kinetic_energy(self):
        return sum(abs(x) for x in self.vel)

    def total_energy(self):
        return self.potential_energy() * self.kinetic_energy()

    
class System(object):

    def __init__(self, moons):
        self.moons = moons.copy()

    def from_text(text):
        moons = []
        for line in text.split("\n"):
            if line:
                m = re.match(r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>", line)
                x = int(m.group(1))
                y = int(m.group(2))
                z = int(m.group(3))
                moons.append(Moon(x, y, z))
        return System(moons)

    def from_file(filename="adv12_input.txt"):
        with open(filename, "r") as f:
            text = f.read()
        return System.from_text(text)

    def __repr__(self):
        return "\n".join([str(m) for m in self.moons])
    
    def step(self):
        # Execute a time step.
        # Consider each pair of moons in the system and calculate
        # the velocity changes on each moon.
        # Then apply the new velocity to each moon to obtain new positions.
        for m1, m2 in itertools.combinations(self.moons, 2):
            for i in range(0,3):
                if m1.pos[i] < m2.pos[i]:
                    m1.vel[i] += 1
                    m2.vel[i] -= 1
                elif m1.pos[i] > m2.pos[i]:
                    m1.vel[i] -= 1
                    m2.vel[i] += 1

        for m in self.moons:
            for i in range(0,3):
                m.pos[i] += m.vel[i]

    def total_energy(self):
        return sum(m.total_energy() for m in self.moons)

    
def part1():
    system = System.from_file()
    for i in range(0,1000):
        system.step()
    print(system.total_energy())
    
