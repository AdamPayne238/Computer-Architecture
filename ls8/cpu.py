"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # PC
        self.pc = 0
        # REGISTER
        self.reg = [0] * 8
        # RAM
        self.ram = [0] * 256


    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

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

    # Memory Address Register (MAR)
    # Memory Data Register (MDR).

    def ram_read(self, MAR):  # should accept the address to read and return the value stored there.
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):  # should accept a value to write, and the address to write it to.
        self.ram[MAR] = MDR

    def run(self):
        """Run the CPU."""

        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001

        running = True

        while running:
            command = self.ram[self.pc]

            # LDI - load "immediate", store a value in a register, or "set this register to this value".
            if command == LDI:
                opperand_a = self.ram_read(self.pc + 1)
                opperand_b = self.ram_read(self.pc + 2)
                self.reg[opperand_a] += opperand_b
                self.pc += 3

            # PRN - a pseudo-instruction that prints the numeric value stored in a register.
            elif command == PRN:
                num = self.ram[self.pc + 1]
                print(self.reg[num])
                self.pc += 2

            # HLT - halt the CPU and exit the emulator.
            elif command == HLT:
                running = False
                self.pc += 1


