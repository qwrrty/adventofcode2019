#! /usr/bin/env python3


def fuel_for_mass(m):
    return max(m // 3 - 2, 0)


class Module:

    def __init__(self, mass=0):
        self.mass = mass

    def required_fuel(self):
        return fuel_for_mass(self.mass)

    def total_required_fuel(self):
        total_fuel = 0
        mass = self.mass
        while mass > 0:
            fuel = fuel_for_mass(mass)
            total_fuel += fuel
            mass = fuel
        return total_fuel


def read_input(filename):
    with open(filename, "r") as f:
        nums = [int(x) for x in f]
    return nums


def part1(module_masses):
    total_fuel = sum([Module(m).required_fuel() for m in module_masses])
    print(total_fuel)


def part2(module_masses):
    total_fuel = sum([Module(m).total_required_fuel() for m in module_masses])
    print(total_fuel)


if __name__ == "__main__":
    input_data = read_input("adv1_input.txt")
    part2(input_data)

