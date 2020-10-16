from cpuBase import CpuBase

class CpuUtility(CpuBase):
    def __init__(self):
        super().__init__()

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

    def trace(self):
            """
            Handy function to print out the CPU state. You might want to call this
            from run() if you need help debugging.
            """

            print(f"TRACE: %02X %02X | %02X %02X %02X |" % (
                self.pc,
                self.fl,
                #self.ie,
                self.ram_read(self.pc),
                self.ram_read(self.pc + 1),
                self.ram_read(self.pc + 2),
            ), end='')

            for i in range(8):
                print(" %02X" % self.reg[i], end='')

            print()