from cpuUtility import CpuUtility
from cpuAlu import CpuAlu
from cpuInteruption import CpuInteruption

class CpuInstructionTable(CpuAlu, CpuInteruption):
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
            0b10000011: self.ld, # Sets a register to a specific spot in memory
            0b10000100: self.st, # Stores a value at a specific spot in memory
            0b01010010: self.intr, # Alters a bit in IM
            # Multiplies two values from register
            0b00010011: self.iret, # Restores all pre interrupt values
            0b01010100: self.jmp, # Manually set's the PC
            0b01001000: self.pra, # Prints a unicode char
            0b01011000: self.jlt, # Changes PC if flag is 4
            0b01010101: self.jeq, # Jump if flag is 1
            0b01010110: self.jne, # Jump if flag is not 1
            # Adds two values together
            0b10100000: lambda opA, opB: self.alu("ADD", opA, opB),
            # Compares two values
            0b10100111: lambda opA, opB: self.alu("CMP", opA, opB),
            # Multiplies two values
            0b10100010: lambda opA, opB: self.alu("MUL", opA, opB), 
            # Divides two values
            0b10100011: lambda opA, opB: self.alu("DIV", opA, opB),
            # Increments two values
            0b01100101: lambda opA, opB: self.alu("INC", opA, opB),
            # Decrements two values
            0b01100110: lambda opA, opB: self.alu("DEC", opA, opB),
            # Bitwise ands two values
            0b10101000: lambda opA, opB: self.alu("AND", opA, opB),
            # Bitwise ors two values
            0b10101010: lambda opA, opB: self.alu("OR", opA, opB),
            # Bitwise xors two values
            0b10101011: lambda opA, opB: self.alu("XOR", opA, opB),
            # Bitwise nots two values
            0b01101001: lambda opA, opB: self.alu("NOT", opA, opB),
            # Bitwise shifts a value left
            0b10101100: lambda opA, opB: self.alu("SHL", opA, opB),
            # Bitwise shifts a value right
            0b10101101: lambda opA, opB: self.alu("SHR", opA, opB),
            # Gets the modulo of two values
            0b10100100: lambda opA, opB: self.alu("MOD", opA, opB),
            # Stops the system from running
            0b00000001: self.hlt,
        }