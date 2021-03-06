#! /usr/bin/env python3

# Implementation of the Intcode computer in Advent of Code 2019

from collections import defaultdict

Opcode = {
     1: {"name": "ADD",      "param_count": 3},
     2: {"name": "MUL",      "param_count": 3},
     3: {"name": "INPUT",    "param_count": 1},
     4: {"name": "OUTPUT",   "param_count": 1},
     5: {"name": "JMPIF",    "param_count": 2},
     6: {"name": "JMPIFNOT", "param_count": 2},
     7: {"name": "LT",       "param_count": 3},
     8: {"name": "EQ",       "param_count": 3},
     9: {"name": "REL",      "param_count": 1},
    99: {"name": "HALT",     "param_count": 1},
}


class ParameterMode(object):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


class Instruction(object):
    def __init__(self, opcode):
        self.opcode = opcode % 100
        self.name = Opcode[self.opcode]["name"]
        self.param_count = Opcode[self.opcode]["param_count"]

        # Decode parameter modes from high order opcode digits
        #
        # Parameter modes are single digits, one per parameter, read
        # right-to-left from the opcode: the first parameter's mode is
        # in the hundreds digit, the second parameter's mode is in the
        # thousands digit, the third parameter's mode is in the
        # ten-thousands digit, and so on. Any missing modes are 0.
        
        n = opcode // 100
        param_mode = []
        for i in range(0, self.param_count):
            param_mode.append(n % 10)
            n = n // 10
        self.param_mode = param_mode

    def __repr__(self):
        return "<Instruction {} param_count={} param_mode={}>".format(
            self.name, self.param_count, self.param_mode)


class Intcode(object):

    OP_ADD      =  1
    OP_MUL      =  2
    OP_INPUT    =  3
    OP_OUTPUT   =  4
    OP_JMPIF    =  5
    OP_JMPIFNOT =  6
    OP_LT       =  7
    OP_EQ       =  8
    OP_REL      =  9
    OP_HALT     = 99

    # Machine states
    RUNNING     = "RUNNING"   # Machine is running or able to start
    BLOCKED     = "BLOCKED"   # Machine is blocked and waiting on input
    HALTED      = "HALTED"    # Machine has halted

    def __init__(self, data, inputs=[]):
        self.pc = 0
        self.memory = defaultdict(int)
        self.inputs = inputs.copy()
        self.outputs = []
        self.relative_base = 0
        self.state = Intcode.RUNNING

        for i in range(0, len(data)):
            self.memory[i] = data[i]

    def from_file(filename, inputs=[]):
        # Class method to generate a new Intcode computer from
        # a program in "filename"
        data = []
        with open(filename, "r") as f:
            for line in f:
                data.extend([int(x) for x in line.split(",")])
        return Intcode(data, inputs)

    def is_running(self):
        return self.state == Intcode.RUNNING

    def is_blocked(self):
        return self.state == Intcode.BLOCKED

    def is_halted(self):
        return self.state == Intcode.HALTED

    def poke(self, addr, num, mode=ParameterMode.POSITION):
        if mode == ParameterMode.RELATIVE:
            self.memory[self.relative_base + addr] = num
        else:
            self.memory[addr] = num

    def peek(self, addr, mode=ParameterMode.IMMEDIATE):
        if mode == ParameterMode.POSITION:
            addr = self.memory[addr]
        elif mode == ParameterMode.RELATIVE:
            addr = self.relative_base + self.memory[addr]
        return self.memory[addr]

    def add_input(self, input_val):
        self.inputs.append(input_val)

    def step(self):
        # Step through executing one instruction in the Intcode program.
        # Returns the opcode just executed.

        # First check whether we are blocked on executing for any reason
        if self.is_halted():
            return Intcode.OP_HALT
        if self.is_blocked() and not self.inputs:
            return Intcode.OP_INPUT
        else:
            # input is available, we're back in business
            self.state = Intcode.RUNNING

        opcode = self.memory[self.pc]
        inst = Instruction(opcode)

        param_start = self.pc + 1
        new_pc = self.pc + 1 + inst.param_count

        if inst.opcode == Intcode.OP_ADD:
            param1 = self.peek(param_start,   mode=inst.param_mode[0])
            param2 = self.peek(param_start+1, mode=inst.param_mode[1])
            param3 = self.peek(param_start+2)
            result = param1 + param2
            self.poke(param3, result,         mode=inst.param_mode[2])
        elif inst.opcode == Intcode.OP_MUL:
            param1 = self.peek(param_start,   mode=inst.param_mode[0])
            param2 = self.peek(param_start+1, mode=inst.param_mode[1])
            param3 = self.peek(param_start+2)
            result = param1 * param2
            self.poke(param3, result,         mode=inst.param_mode[2])
        elif inst.opcode == Intcode.OP_INPUT:
            # If no input is available, set the machine state to BLOCKED
            # and return immediately (do not advance the PC counter)
            if not self.inputs:
                self.state = Intcode.BLOCKED
                return None
            result = self.inputs.pop(0)
            param1 = self.peek(param_start)
            self.poke(param1, result,         mode=inst.param_mode[0])
        elif inst.opcode == Intcode.OP_OUTPUT:
            param1 = self.peek(param_start,   mode=inst.param_mode[0])
            self.outputs.append(param1)
        elif inst.opcode == Intcode.OP_JMPIF:
            param1 = self.peek(param_start,   mode=inst.param_mode[0])
            param2 = self.peek(param_start+1, mode=inst.param_mode[1])
            if param1:
                new_pc = param2
        elif inst.opcode == Intcode.OP_JMPIFNOT:
            param1 = self.peek(param_start,   mode=inst.param_mode[0])
            param2 = self.peek(param_start+1, mode=inst.param_mode[1])
            if not param1:
                new_pc = param2
        elif inst.opcode == Intcode.OP_LT:
            param1 = self.peek(param_start,   mode=inst.param_mode[0])
            param2 = self.peek(param_start+1, mode=inst.param_mode[1])
            param3 = self.peek(param_start+2)
            self.poke(param3, 1 if param1 < param2 else 0, mode=inst.param_mode[2])
        elif inst.opcode == Intcode.OP_EQ:
            param1 = self.peek(param_start,   mode=inst.param_mode[0])
            param2 = self.peek(param_start+1, mode=inst.param_mode[1])
            param3 = self.peek(param_start+2)
            self.poke(param3, 1 if param1 == param2 else 0, mode=inst.param_mode[2])
        elif inst.opcode == Intcode.OP_REL:
            param1 = self.peek(param_start,   mode=inst.param_mode[0])
            self.relative_base += param1
        elif inst.opcode == Intcode.OP_HALT:
            self.state = Intcode.HALTED
        else:
            raise Exception("unknown opcode {}".format(inst.opcode))

        self.pc = new_pc
        return inst.opcode

    def run(self, break_on_output=0):
        # Run an Intcode program.
        # If break_on_output is nonzero, return outputs as soon as
        # this many outputs has been received.
        # If the program halts, return None.
        while True:
            self.step()
            if break_on_output and len(self.outputs) >= break_on_output:
                result = self.outputs[0:break_on_output]
                self.outputs = self.outputs[break_on_output:]
                return result
            if not self.is_running():
                # Machine is blocked or halted
                break
        return None
