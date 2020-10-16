class CpuBase:
    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0,0,0,0,0,0,0,0xf4]
        self.pc = 0
        self.fl = 0
    
    """ Method to read ram """
    def ram_read(self, pointer):
        return self.ram[pointer]

    """ Method to write to ram """
    def ram_write(self, pointer, value):
        self.ram[pointer] = value

    """ Removes the current item from the stack and stores it in the provided register """
    def pop(self, opA, opB):
        # print('self.reg[7]: ', self.reg[7])
        value = self.ram_read(self.reg[7])
        self.reg[opA] = value
        self.reg[7] += 1

    """ Adds a value onto the stack from the provided register """
    def push(self, opA, opB):
        print('opA: ', opA)
        self.reg[7] -= 1
        self.ram_write(self.reg[7], self.reg[opA])

    """ Set's the PC as the last element in the stack """
    def ret(self, opA, opB):
        self.pc = self.ram_read(self.reg[7])
        self.reg[7] += 1

    """ Set's the PC as the value provided and stores the old PC on the stack """
    def call(self, opA, opB):
        self.reg[7] -= 1
        self.ram_write(self.reg[7], self.pc + 2)
        self.pc = self.reg[opA]

    """ Stores value in memory """
    def st(self, regA, regB):
        self.ram_write(self.reg[regA], self.reg[regB])
    
    def jmp(self, opA, opB):
        self.pc = self.reg[opA]
    
    def jlt(self, opA, opB):
        if self.fl == 4:
            self.pc = self.reg[opA]
        else:
            self.pc += 2
    
    def jeq(self, opA, opB):
        if self.fl == 1:
            self.pc = self.reg[opA]
        else:
            self.pc += 2

    def jne(self, opA, opB):
        if (self.fl & 0b00000001) == 0:
            self.pc = self.reg[opA]
        else:
            self.pc += 2

    def pra(self, opA, opB):
        print(chr(self.reg[opA]), end = "", flush=True)

    """ Stores a value in the register """
    def ldi(self, opA, opB):
        self.reg[opA] = opB

    """ Prints a value in the register """
    def prn(self, opA, opB):
        print(self.reg[opA])