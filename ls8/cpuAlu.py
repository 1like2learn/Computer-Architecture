from cpuBase import CpuBase

class CpuAlu(CpuBase):
    def __init__(self):
        super().__init__()

    """ Function that does mathematical operations. """
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        def add():
            self.reg[reg_a] += self.reg[reg_b]
        def sub():
            self.reg[reg_a] -= self.reg[reg_b]
        def mul():
            self.reg[reg_a] *=  self.reg[reg_b]
        def comp():
            if self.reg[0] > self.reg[1]:
                self.fl = 4
            elif self.reg[0] > self.reg[1]:
                self.fl = 2
            else:
                self.fl = 1
        switchTable = {
            "ADD": add,
            "SUB": sub,
            "MUL": mul,
            "CMP": comp,
        }
        if op not in switchTable:
            raise Exception("Unsupported ALU operation")
        switchTable[op]()