#! /usr/bin/env python3

class Intcode(object):

    OP_ADD = 1
    OP_MUL = 2
    OP_HALT = 99

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


def part1(program):
    code = Intcode(program)
    code.poke(1, 12)
    code.poke(2, 2)
    code.run()
    print(code.peek(0))


def part2(program, target=19690720):
    for i in range(0, 99):
        for j in range(0, 99):
            code = Intcode(program)
            code.poke(1, i)
            code.poke(2, j)
            code.run()
            print("noun={} verb={} output={}".format(i, j, code.peek(0)))
            if code.peek(0) == target:
                print("FOUND: noun={} verb={} result={}".format(i, j, i*100 + j))
                return
            if code.peek(0) > target:
                break
    print("No solution found")
    

def read_input(filename):
    data = []
    with open(filename, "r") as f:
        for line in f:
            data.extend([int(x) for x in line.split(",")])
    return data

if __name__ == "__main__":
    data = read_input("adv2_input.txt")
    print(data)
    part2(data, target=1202)
