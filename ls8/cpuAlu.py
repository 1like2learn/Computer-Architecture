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
        def div():
            self.reg[reg_a] /= self.reg[reg_b]
        def inc():
            self.reg[reg_a] += 1
        def dec():
            self.reg[reg_a] -= 1
        def comp():
            if self.reg[reg_a] < self.reg[reg_b]:
                self.fl = 4
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl = 2
            else:
                self.fl = 1
        def andOp():
            self.reg[reg_a] &= self.reg[reg_b]
        def orOp():
            self.reg[reg_a] |= self.reg[reg_b]
        def xor():
            self.reg[reg_a] ^= self.reg[reg_b]
        def notOp():
            self.reg[reg_a] = ~ self.reg[reg_a]
        def shl():
            self.reg[reg_a] <<= self.reg[reg_b]
        def shr():
            self.reg[reg_a] >>= self.reg[reg_b]
        def mod():
            self.reg[reg_a] %= self.reg[reg_b]


        switchTable = {
            "ADD": add,
            "SUB": sub,
            "MUL": mul,
            "DIV": div,
            "CMP": comp,
            "INC": inc,
            "DEC": dec,
            "AND": andOp,
            "OR": orOp,
            "XOR": xor,
            "NOT": notOp,
            "SHL": shl,
            "SHR": shr,
            "MOD": mod,
        }
        if op not in switchTable:
            raise Exception("Unsupported ALU operation")
        switchTable[op]()