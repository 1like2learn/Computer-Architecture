"""CPU functionality."""

import sys

import datetime
from cpuUtility import CpuUtility
from cpuAlu import CpuAlu

class CPU(CpuUtility, CpuAlu):
    """Main CPU class."""
    def __init__(self):
        super().__init__()
        self.branchTable = {
            0b10000010: self.ldi, # Stores value in register
            0b01000111: self.prn, # Prints value from register
            0b01000101: self.push, # Stores a value on stack
            0b01000110: self.pop, # Returns value from stack
            0b01010000: self.call, # Runs code from a different part of the instructions
            0b00010001: self.ret, # Returns to where you were at after call
            0b10000100: self.st, # Stores a value at a specific spot in memory
            0b01010010: self.intr, # Alters a bit in 
            # Multiplies two values from register
            0b10100010: lambda opA, opB: self.alu("MUL", opA, opB), 
            # Adds two values together
            0b10100000: lambda opA, opB: self.alu("ADD", opA, opB),
            # Compares two values
            0b10100111: lambda opA, opB: self.alu("CMP", opA, opB),

        }
    
    """ Add a interrupt bit to R6 """
    def intr(self, opA, opB):
        result = pow(2, opA)
        self.reg[6] = result | self.reg[6]

    """ Set's the PC as the last element in the stack """
    def ret(self, opA, opB):
        self.reg[7] +=1
        self.pc = self.ram_read(self.reg[7])
        # print('self.reg[7]: ', self.reg[7])
        # print(self.ram[240:245])

    """ Set's the PC as the value provided and stores the old PC on the stack """
    def call(self, opA, opB):
        self.push(self.pc + 2, opB)
        self.pc = self.reg[opA]

    """ Swaps values in registers """
    def st(self, regA, regB):
        self.ram_write(self.reg[regA], self.reg[regB])

    def run(self):
        """Run the CPU."""
        HLT = 0b00000001 # 1
        halt = False

        while not halt:
            # self.trace()
            ir = self.ram[self.pc] # Instruction register
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir == HLT:
                halt = True
            else:
                """
                If the command is not HLT use run the function in 
                the branchtable with the key being the current instruction. 
                """
                self.branchTable[ir](operand_a, operand_b)

            """
            Increment the PC commensurate to the value of the first two 
            digits in the instruction plus one
            """
            if (ir & 0b00010000) >> 4 == 0:
                instruction_len = (ir >> 6) + 1
                self.pc += instruction_len
