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
        def inc():
            self.reg[reg_a] += 1
        def comp():
            if self.reg[reg_a] < self.reg[reg_b]:
                self.fl = 4
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl = 2
            else:
                self.fl = 1
        switchTable = {
            "ADD": add,
            "SUB": sub,
            "MUL": mul,
            "CMP": comp,
            "INC": inc
        }
        if op not in switchTable:
            raise Exception("Unsupported ALU operation")
        switchTable[op]()