#! /usr/bin/env python3

# Implementation of the Intcode computer as specified in Day 5


from enum import Enum

class Opcode(Enum):
    ADD    =  1
    MUL    =  2
    INPUT  =  3
    OUTPUT =  4
    HALT   = 99


InstructionSet = {
    Opcode.ADD: {"param_count": 3},
    Opcode.MUL: {"param_count": 3},
    Opcode.INPUT: {"param_count": 1},
    Opcode.OUTPUT: {"param_count": 1},
    Opcode.HALT: {"param_count": 1},
}


class Instruction(object):
    def __init__(self, opcode):
        self.opcode = opcode % 100
        self.param_count = InstructionSet[opcode]["param_count"]

        # Decode parameter modes from high order opcode digits
        #
        # Parameter modes are single digits, one per parameter, read
        # right-to-left from the opcode: the first parameter's mode is
        # in the hundreds digit, the second parameter's mode is in the
        # thousands digit, the third parameter's mode is in the
        # ten-thousands digit, and so on. Any missing modes are 0.
        
        n = opcode // 100
        param_modes = []
        for i in range(0, self.param_count):
            param_modes.append(n % 10)
            n = n // 10
        self.param_modes = param_modes
        

        
class Intcode(object):

    OP_ADD    =  1
    OP_MUL    =  2
    OP_INPUT  =  3
    OP_OUTPUT =  4
    OP_HALT   = 99

    def __init__(self, data):
        self.pc = 0
        self.memory = data.copy()

    def poke(self, addr, num):
        self.memory[addr] = num
    
    def peek(self, addr):
        return self.memory[addr]
    
    def step(self):
        opcode = self.memory[self.pc]
        inst = Instruction.decode(opcode)
        param_start = self.pc + 1
        param_end = inst.param_count
        params = self.memory[param_start:param_end]
        
        if opcode == Intcode.OP_ADD:
            addr1, addr2, addr3 = self.memory[self.pc+1:self.pc+4]
            self.memory[addr3] = self.memory[addr1] + self.memory[addr2]
            self.pc += 4
        elif opcode == Intcode.OP_MUL:
            addr1, addr2, addr3 = self.memory[self.pc+1:self.pc+4]
            self.memory[addr3] = self.memory[addr1] * self.memory[addr2]
            self.pc += 4
        elif opcode == Intcode.OP_HALT:
            return False
        return True

    def run(self):
        while self.step():
            pass


