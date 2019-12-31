#! /usr/bin/env python3

class FFT(object):
    
    def __init__(self, input_list):
        self.input_list = [int(d) for d in input_list]

    def from_file(filename="adv16_input.txt"):
        with open(filename, "r") as f:
            return FFT(f.read().strip())

    def phase_pattern_generator(self, phase):
        vals = [0] * (phase-1)
        while True:
            for n in vals:
                yield n
            for n in [1] * phase:
                yield n
            for n in [0] * phase:
                yield n
            for n in [-1] * phase:
                yield n
            vals = [0] * phase

    def fft(self, max_phase=1):
        current_list = self.input_list
        for phase in range(1, max_phase+1):
            pc = 1
            output_list = []
            for _ in current_list:
                pattern = self.phase_pattern_generator(pc)
                total = 0
                for digit in current_list:
                    total += digit * next(pattern)
                output_list.append(abs(total) % 10)
                pc += 1
            current_list = output_list

        return "".join([str(ch) for ch in current_list])


def part1():
    print(FFT.from_file().fft(max_phase=100)[0:8])
