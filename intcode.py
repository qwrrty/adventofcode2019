#! /usr/bin/env python3

# Implementation of the Intcode computer as specified in Day 5


Opcode = {
     1: {"name": "ADD",      "param_count": 3},
     2: {"name": "MUL",      "param_count": 3},
     3: {"name": "INPUT",    "param_count": 1},
     4: {"name": "OUTPUT",   "param_count": 1},
     5: {"name": "JMPIF",    "param_count": 2},
     6: {"name": "JMPIFNOT", "param_count": 2},
     7: {"name": "LT",       "param_count": 3},
     8: {"name": "EQ",       "param_count": 3},
    99: {"name": "HALT",     "param_count": 1},
}


class ParameterMode(object):
    POSITION = 0
    IMMEDIATE = 1


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
    OP_HALT     = 99

    def __init__(self, data):
        self.pc = 0
        self.memory = data.copy()

    def poke(self, addr, num):
        self.memory[addr] = num
    
    def peek(self, addr, mode=ParameterMode.IMMEDIATE):
        if mode == ParameterMode.POSITION:
            addr = self.memory[addr]
        return self.memory[addr]
    
    def step(self):
        opcode = self.memory[self.pc]
        inst = Instruction(opcode)

        param_start = self.pc + 1
        new_pc = self.pc + 1 + inst.param_count
        
        if inst.opcode == Intcode.OP_ADD:
            param1 = self.peek(param_start,   mode=inst.param_mode[0])
            param2 = self.peek(param_start+1, mode=inst.param_mode[1])
            param3 = self.peek(param_start+2)
            result = param1 + param2
            self.poke(param3, result)
        elif inst.opcode == Intcode.OP_MUL:
            param1 = self.peek(param_start,   mode=inst.param_mode[0])
            param2 = self.peek(param_start+1, mode=inst.param_mode[1])
            param3 = self.peek(param_start+2)
            result = param1 * param2
            self.poke(param3, result)
        elif inst.opcode == Intcode.OP_INPUT:
            param1 = self.peek(param_start)
            result = int(input("intcode> "))
            self.poke(param1, result)
        elif inst.opcode == Intcode.OP_OUTPUT:
            param1 = self.peek(param_start, mode=inst.param_mode[0])
            print(param1)
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
            self.poke(param3, 1 if param1 < param2 else 0)
        elif inst.opcode == Intcode.OP_EQ:
            param1 = self.peek(param_start,   mode=inst.param_mode[0])
            param2 = self.peek(param_start+1, mode=inst.param_mode[1])
            param3 = self.peek(param_start+2)
            self.poke(param3, 1 if param1 == param2 else 0)
        elif inst.opcode == Intcode.OP_HALT:
            return False
        else:
            raise Exception("unknown opcode {}".format(inst.opcode))

        self.pc = new_pc
        return True

    def run(self):
        while self.step():
            pass
