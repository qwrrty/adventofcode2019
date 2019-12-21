#! /usr/bin/env python3

import itertools

from intcode import Intcode


def run_amps_with_phase_settings(program, phase_settings):
    input_val = 0

    for i in phase_settings:
        machine_inputs = [i, input_val]
        intcode = Intcode(program, machine_inputs)
        result = intcode.run()
        input_val = intcode.outputs[0]
    return intcode.outputs[0]


def run_all(program):
    # Generate a list of inputs sorted from largest to smallest
    best_result = 0
    for p in itertools.permutations("01234", 5):
        phase_settings = [int(n) for n in p]
        result = run_amps_with_phase_settings(program, phase_settings)
        if result > best_result:
            best_result = result

    return best_result


def read_intcode(filename):
    program = []
    with open(filename, "r") as f:
        for line in f:
            program.extend([int(x) for x in line.split(",")])
    return program


def part1(filename="adv7_input.txt"):
    program = read_intcode(filename)
    result = run_all(program)
    print(result)
