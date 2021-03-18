"""CPU functionality."""

import sys
import time
from pynput import keyboard

from cpuInstructionTable import CpuInstructionTable

class CPU(CpuInstructionTable):
    """Main CPU class."""
    def __init__(self):
        super().__init__()

    def run(self):
        """Run the CPU."""

        prevCycle = time.time()
        
        while not self.halt:

            if self.reg[5]:
                with keyboard.Events() as events:
                    self.ram_write(0xf4, 0)
                    event = events.get(0.10)
                    if event and type(event.key) == str:
                        self.ram_write(event.key, 0xf4)
                if int(time.time() - prevCycle) >= 1:
                    self.reg[6] = self.reg[6] | 1
                    prevCycle = time.time()
                if self.ram_read(0xf4) != 0:
                    self.reg[6] = self.reg[6] | 2

                maskedInterupts = self.reg[6] & self.reg[5]
                if maskedInterupts and self.ie:
                    self.interupt(maskedInterupts)

            ir = self.ram[self.pc] # Instruction register
            opA = self.ram_read(self.pc + 1)
            opB = self.ram_read(self.pc + 2)
            # self.trace()

            if ir in self.branchTable:
                """
                Run the function in the branchtable with the key being the current instruction. 
                """
                self.branchTable[ir](opA, opB)
            else: 
                print(f"Instruction at: {self.pc}: {ir} is not a valid instruction")
                self.halt = True
            """
            Increment the PC commensurate to the value of the first two 
            digits in the instruction plus one
            """
            if (ir & 0b00010000) >> 4 == 0:
                instruction_len = (ir >> 6) + 1
                self.pc += instruction_len