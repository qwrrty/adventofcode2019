#! /usr/bin/env python3

# Implementation of the Intcode computer as specified in Day 5

class Intcode(object):

    OP_ADD    =  1
    OP_MUL    =  2
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


