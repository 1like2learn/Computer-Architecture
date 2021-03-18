# from cpuBase import CpuBase
from cpuUtility import CpuUtility

import math

class CpuInteruption(CpuUtility):
    def __init__(self):
        super().__init__()

    def interupt(self, mi):
        self.ie = False
        self.reg[7] -= 1
        self.ram_write(self.reg[7], self.pc)
        self.reg[7] -= 1
        self.ram_write(self.reg[7], self.fl)
        for reg in range(0,7):
            self.reg[7] -= 1
            self.ram_write(self.reg[7], self.reg[reg])
        self.pc = self.ram_read(int(math.log(mi, 2)) + 0xf8)
        self.reg[6] = 0

    
    """
    For registers 6-0 assign their old value from the stack.
    Grab FL's and PC's value from the stack. Reset the IS
    """
    def iret(self, opA, opB):
        for reg in range(0,7):
            reg = abs(reg - 6)
            self.reg[reg] = self.ram_read(self.reg[7])
            self.reg[7] += 1
        self.fl = self.ram_read(self.reg[7])
        self.reg[7] += 1
        self.pc = self.ram_read(self.reg[7])
        self.reg[7] += 1
        self.reg[6] = 0
        self.ie = True

    """ Add a interrupt bit to R6 """
    def intr(self, opA, opB):
        result = pow(2, opA)
        self.reg[6] = result | self.reg[6]
