"""CPU functionality."""

import sys
import time

from cpuUtility import CpuUtility
from cpuAlu import CpuAlu
from cpuInteruption import CpuInteruption

class CPU(CpuAlu, CpuInteruption):
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
            0b01010010: self.intr, # Alters a bit in IM
            # Multiplies two values from register
            0b10100010: lambda opA, opB: self.alu("MUL", opA, opB), 
            # Adds two values together
            0b10100000: lambda opA, opB: self.alu("ADD", opA, opB),
            # Compares two values
            0b10100111: lambda opA, opB: self.alu("CMP", opA, opB),
            0b00010011: self.iret, # Restores all pre interrupt values
            0b01010100: self.jmp, # Manually set's the PC
            0b01001000: self.pra, # Prints a unicode char
            0b01011000: self.jlt, # Changes PC if flag is 4
            0b01100101: lambda opA, opB: self.alu("INC", opA, opB),
            0b01010101: self.jeq,
            0b01010110: self.jne,
        }

    def run(self):
        """Run the CPU."""
        HLT = 0b00000001 # 1
        self.halt = False
        prevCycle = time.time()
        interuptable = True
        
        while not self.halt:
            if self.reg[5]:
                if int(time.time() - prevCycle) >= 1:
                    self.reg[6] = self.reg[6] | 1
                    prevCycle = time.time()
                maskedInterupts = self.reg[6] & self.reg[5]
                if maskedInterupts and interuptable:
                    interuptable = False
                    self.interupt(maskedInterupts)
            ir = self.ram[self.pc] # Instruction register
            opA = self.ram_read(self.pc + 1)
            opB = self.ram_read(self.pc + 2)
            self.trace()
            if ir == HLT:
                self.halt = True
            else:
                """
                If the command is not HLT run the function in 
                the branchtable with the key being the current instruction. 
                """
                self.branchTable[ir](opA, opB)
            if ir == 0b00010011: # IRET
                interuptable = True
            """
            Increment the PC commensurate to the value of the first two 
            digits in the instruction plus one
            """
            if (ir & 0b00010000) >> 4 == 0:
                instruction_len = (ir >> 6) + 1
                self.pc += instruction_len
