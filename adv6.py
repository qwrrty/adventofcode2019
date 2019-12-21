#! /usr/bin/env python3


from collections import defaultdict


class OrbitMap(object):
    def __init__(self, data):
        self.orbits = defaultdict(set)
        for orbit in data:
            body1, body2 = orbit.strip().split(")")
            self.orbits[body1].add(body2)

    def sum_orbits(self, starting_body="COM", depth=0):
        # The number of orbits for this body is defined as its depth in the tree
        total_orbits = depth
        for body in self.orbits[starting_body]:
            total_orbits += self.sum_orbits(body, depth+1)
        return total_orbits

    def find_body(self, target, starting_body="COM"):
        # Return the list of bodies in the tree between a starting body and target
        if target == starting_body:
            return [target]
        for body in self.orbits[starting_body]:
            path = self.find_body(target, body)
            if path:
                return [starting_body] + path
        # If we got here, no valid paths were found
        return list()
    
    
def read_input(filename):
    with open(filename, "r") as f:
        data = f.readlines()
    return data


def part1(orbits):
    print(orbits.sum_orbits())


def part2(orbits, target1, target2):
    path1 = orbits.find_body(target1)
    path2 = orbits.find_body(target2)

    # Find out where the two paths diverge
    for i in range(0, len(path1)):
        if path1[i] != path2[i]:
            # The paths have diverged. The transit distance is the number of
            # bodies remaining in path1 plus the number of bodies remaining
            # in path2.
            return len(path2[i:-1]) + len(path1[i:-1])
        

if __name__ == "__main__":
    data = read_input("adv6_input.txt")
    orbits = OrbitMap(data)
    part2(orbits, "YOU", "SAN")
