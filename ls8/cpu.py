"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.pc = 0
        self.registers = [0] * 8

        self.branchtable = {}
        self.branchtable[0b00000001] = self.handle_hlt
        self.branchtable[0b10000010] = self.handle_ldi
        self.branchtable[0b01000111] = self.handle_prn
        self.branchtable[0b10100010] = self.handle_mul

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self, filename):
        """Load a program into memory."""

        program = []

        try:
            with open(filename) as f:
                for line in f:
                    comment_split = line.split("#")
                    num = comment_split[0].strip()
                    if len(num) == 0:
                        continue
                    value = int(num, 2)
                    program.append(value)

        except FileNotFoundError:
            print(f"{filename} not found")
            sys.exit(2)

        address = 0

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

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

    def handle_hlt(self, operand_a, operand_b):
        sys.exit(0)

    def handle_ldi(self, operand_a, operand_b):
        self.registers[operand_a] = operand_b

    def handle_prn(self, operand_a, operand_b):
        print(self.registers[operand_a])

    def handle_mul(self, operand_a, operand_b):
        self.registers[operand_a] *=  self.registers[operand_b]

    def run(self):
        """Run the CPU."""
        while True:
            ir = self.ram[self.pc]
            operand_a = self.ram[self.pc + 1]
            operand_b = self.ram[self.pc + 2]


            ops_to_skip = (ir >> 6) + 1

            self.branchtable[ir](operand_a, operand_b)
            
            self.pc += ops_to_skip
