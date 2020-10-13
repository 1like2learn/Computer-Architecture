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
            0b10000010: self.ldi, 
            0b01000111: self.prn, 
            0b10100010: lambda opA, opB: self.alu("MULT", opA, opB),
            0b01000101: self.push,
            0b01000110: self.pop,
            0b01010000: self.call,
            0b00010001: self.ret,
            0b10100000: lambda opA, opB: self.alu("ADD", opA, opB),
        }

    def load(self, openFile):
        """Load a program into memory."""

        address = 0
        program = []

        """
        Open a the provided file. Check if the current line is a 
        comment or empty line. If it's not take the first 8 indices 
        and type cast them as a binary number.
        """
        f = open(openFile, "r")
        for line in f:
            if len(line) < 2 or line[0] == "#":
                continue
            program.append(int(line[:8], base = 2))
        f.close()
        
        """
        Add each line to the program list.
        """
        for instruction in program:
            # print('instruction: ', instruction)
            self.ram_write(address, instruction)
            address += 1

    """ Function that does mathematical operations. """
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *=  self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    """ Method to read ram """
    def ram_read(self, pointer):
        return self.ram[pointer]

    """ Method to write to ram """
    def ram_write(self, pointer, value):
        self.ram[pointer] = value

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

    """ Removes the current item from the stack and stores it in the provided register """
    def pop(self, operand_a, operand_b):
        if self.reg[7] == 0 or self.reg[7] == 0xf3:
            print("There is nothing in the stack to remove")
        self.reg[7] += 1
        value = self.ram_read(self.reg[7])
        self.reg[operand_a] = value

    """ Adds a value onto the stack from the provided register """
    def push(self, operand_a, operand_b):
        if self.reg[7] == 0:
            self.reg[7] = 0xf3
        # print('self.reg[7]: ', self.reg[7])
        self.ram_write(self.reg[7], operand_a)
        self.reg[7] -= 1

    """ Set's the PC as the last element in the stack """
    def ret(self, operand_a, operand_b):
        self.reg[7] +=1
        self.pc = self.ram_read(self.reg[7])
        # print('self.reg[7]: ', self.reg[7])
        # print(self.ram[240:245])

    """ Set's the PC as the value provided and stores the old PC on the stack """
    def call(self, operand_a, operand_b):
        self.push(self.pc + 1, operand_b)
        self.pc = self.reg[operand_a]


    """ Stores a value in the register """
    def ldi(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b

    """ Prints a value in the register """
    def prn(self, operand_a, operand_b):
        # location = self.ram_read(operand_a)
        print(self.reg[operand_a])

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
            if ir != 0b01010000:
                instruction_len = (ir >> 6) + 1
                self.pc += instruction_len
