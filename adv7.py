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


def run_amps_with_feedback_loop(program, phase_settings):
    # Set up the array of amps each with its phase setting
    amps = []
    for i in phase_settings:
        amps.append(Intcode(program, [i]))

    # The first amp starts with input 0
    amps[0].add_input(0)

    i = 0
    final_output = 0
    while True:
        output = amps[i].run(break_on_output=True)
        if i == 4:
            if output is None:
                # The last amp program halted, so we're done
                break
            # Not yet done, save the output in case we need it
            final_output = output
        i = (i + 1) % 5
        amps[i].add_input(output)

    return final_output
        

def run_with_feedback_loop(program):
    # Generate a list of inputs sorted from largest to smallest
    best_result = 0
    for p in itertools.permutations("56789", 5):
        phase_settings = [int(n) for n in p]
        result = run_amps_with_feedback_loop(program, phase_settings)
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

def part2(filename="adv7_input.txt"):
    program = read_intcode(filename)
    result = run_with_feedback_loop(program)
    print(result)
