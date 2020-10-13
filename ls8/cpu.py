"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.branchTable = {
            0b10000010: self.LDI, 
            0b01000111: self.PRN, 
            0b10100010: self.alu

        }

    def load(self, openFile):
        """Load a program into memory."""

        address = 0
        program = []


        f = open(openFile, "r")
        for line in f:
            if len(line) < 2 or line[0] == "#":
                continue
            program.append(int(line[:8], base = 2))
        f.close()

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        for instruction in program:
            self.ram_write(address, instruction)
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *=  self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")
        return 3

    def ram_read(self, pointer):
        return self.ram[pointer]

    def ram_write(self, pointer, value):
        if pointer >= 0 or pointer < 8:
            self.ram[pointer] = value
        else:
            print(f'There is no memory location at {pointer}')

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
    def LDI(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
        return 3
    def PRN(self, operand_a, operand_b):
        # location = self.ram_read(operand_a)
        print(self.reg[operand_a])
        return 2

    def run(self):
        """Run the CPU."""
        HLT = 0b00000001 # 1
        halt = False
        while not halt:
            IR = self.ram[self.pc] # Instruction register
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR == HLT:
                halt = True
                self.pc +=1
            else:
                self.pc += self.branchTable[IR](operand_a, operand_b)

                


