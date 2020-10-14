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
        if self.reg[7] == 0 or self.reg[7] == 0xf3:
            print("There is nothing in the stack to remove")
        self.reg[7] += 1
        value = self.ram_read(self.reg[7])
        self.reg[opA] = value

    """ Adds a value onto the stack from the provided register """
    def push(self, opA, opB):
        if self.reg[7] == 0:
            self.reg[7] = 0xf3
        # print('self.reg[7]: ', self.reg[7])
        self.ram_write(self.reg[7], opA)
        self.reg[7] -= 1