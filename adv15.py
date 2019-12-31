#! /usr/bin/env python3

from intcode import Intcode


class Direction(object):
    NORTH = 1
    SOUTH = 2
    WEST  = 3
    EAST  = 4

    OPPOSITE = [
        0,
        SOUTH,
        NORTH,
        EAST,
        WEST,
    ]
    
    def move(pos, direction):
        x, y = pos
        if direction == Direction.NORTH:
            return (x, y-1)
        elif direction == Direction.SOUTH:
            return (x, y+1)
        elif direction == Direction.WEST:
            return (x-1, y)
        elif direction == Direction.EAST:
            return (x+1, y)
        else:
            raise Exception("unknown direction {}", direction)

class RepairDroid(object):

    def __init__(self, intcode):
        self.intcode = intcode
        self.ship_map = {}

    def from_file(filename="adv15_input.txt"):
        intcode = Intcode.from_file(filename)
        return RepairDroid(intcode)

    def step(self, pos=(0,0), return_direction=0):
        for d in [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]:
            # Don't explore a square we've already explored, that's silly
            new_pos = Direction.move(pos, d)
            if new_pos in self.ship_map:
                continue
            # Attempt to move in this direction and find out what happens
            self.intcode.add_input(d)
            result = self.intcode.run(break_on_output=1)
            if result[0] == 0:
                # Wall
                self.ship_map[new_pos] = "#"
                continue
            if result[0] == 1:
                # Empty
                self.ship_map[new_pos] = "."
            elif result[0] == 2:
                # Oxygen system
                self.ship_map[new_pos] = "O"
            else:
                raise Exception("got unknown intcode result {}".format(result))
            self.step(new_pos, return_direction=Direction.OPPOSITE[d])
        # If we got here, we are done exploring this part of the map and should return
        self.intcode.add_input(return_direction)
        self.intcode.run(break_on_output=1)

    def bfs(self, start, target="O"):
        # Perform a breadth-first search of the map, beginning at start,
        # seeking for a cell marked with the target char. If target is None
        # then walk the entire map, returning the maximum number of steps.
        steps = 0
        current_points = [start]
        visited = set()

        while current_points:
            next_steps = []
            for p in current_points:
                if target and self.ship_map[p] == target:
                    print(steps)
                    return
                if p in visited:
                    continue
                visited.add(p)
                # Identify the neighbor cells of this point
                neighbors = [Direction.move(p, d) for d in
                             [Direction.NORTH,
                              Direction.SOUTH,
                              Direction.WEST,
                              Direction.EAST]]
                # Limit to neighbors that can be traveled and have not been visited
                valid_neighbors = [p for p in neighbors
                                   if self.ship_map[p] != "#" and p not in visited]
                next_steps.extend(valid_neighbors)
            steps += 1
            current_points = next_steps
            
        # If we got here, we traversed the entire map without finding the target.
        # Return the number of steps walked (which was actually the previous step,
        # the last one in which there were cells to fill)
        return steps-1

    def render_map(self):
        if not self.ship_map:
            return
        
        min_x = min(p[0] for p in self.ship_map)
        min_y = min(p[1] for p in self.ship_map)
        max_x = max(p[0] for p in self.ship_map)
        max_y = max(p[1] for p in self.ship_map)

        rows = []
        for y in range(min_y, max_y+1):
            row = [self.ship_map.get((x,y), " ") for x in range(min_x, max_x+1)]
            rows.append("".join(row))
        output = "\n".join(rows)
        return output

    
def part1():
    droid = RepairDroid.from_file()
    droid.ship_map[(0,0)] = "X"
    droid.step()

    # Perform a breadth-first search of the map to find the shortest
    # path to the oxygen system.
    print(droid.bfs(start=(0,0)))

def part2():
    droid = RepairDroid.from_file()
    droid.ship_map[(0,0)] = "X"
    droid.step()

    # Perform a breadth-first search of the map, starting from the
    # oxygen system, to find out how long it will take the map to
    # fill with oxygen.
    oxygen_system = [p for p, val in droid.ship_map.items() if val == "O"][0]
    print(droid.bfs(start=oxygen_system, target=None))

if __name__ == "__main__":
    part2()
