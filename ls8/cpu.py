"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.flag = 0b00000000

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value



    def load(self):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) != 2:
	        print("usage: ls8.py progname")
	        sys.exit(1)
        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        try:
            with open(sys.argv[1]) as f:
                print(sys.argv[1])
                for instruction in f:
                    instruction = instruction.strip()

                    if instruction == '' or instruction[0] == "#":
                        continue

                    try:
                        str_value = instruction.split("#")[0]
                        value = int(str_value, 2)

                    except ValueError:
                        print(f"Invalid number: {str_value}")
                        sys.exit(1)

                    self.ram[address] = value
                    address += 1

    

        except FileNotFoundError:
            print(f"File not found: {sys.argv[1]}")
            sys.exit(2)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]

        elif op == "CMP":
            if reg_a == reg_b:#E flag is true
                self.flag = 0b00000001
            if reg_a != reg_b:
                self.flag = 0b00000000
            if reg_a < reg_b:
                self.flag = 0b00000100
            if reg_a > reg_b:
                self.flag = 0b00000010

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

    def run(self):
        """Run the CPU."""
        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010
        ADD = 0b10100000
        SUB = 0b10100001

        SP = 7
        PUSH = 0b01000101
        POP = 0b01000110

        CALL = 0b01010000
        RET = 0b00010001
        CMP = 0b10100111
        JMP = 0b01010100
        JNE = 0b01010110
        JEQ = 0b01010101



        self.running = True

        while self.running:
            register = self.ram_read(self.pc)
            operandA = self.ram_read(self.pc + 1)
            operandB = self.ram_read(self.pc + 2)
        
            if register == HLT:
                self.running = False
                self.pc += 1

            elif register == PRN:
                print(self.reg[operandA])
                self.pc += 2

            elif register == LDI:
                self.reg[operandA] = operandB
                self.pc += 3

            elif register == MUL:
                self.alu("MUL", operandA, operandB)
                self.pc += 3

            elif register == ADD:
                self.alu("ADD", operandA, operandB)
                self.pc += 3

            elif register == SUB:
                self.alu("SUB", operandA, operandB)
                self.pc += 3

            elif register == PUSH:
                SP -= 1
                self.ram_write(SP, self.reg[operandA])
                self.pc += 2

            elif register == POP:
                self.reg[operandA] = self.ram[SP]
                SP += 1
                self.pc += 2

            elif register == CALL:
                value = self.pc + 2
                SP -= 1
                self.ram_write(SP, value)
                self.pc = self.reg[operandA]

            elif register == RET:
                self.pc = self.ram[SP]
                SP += 1

            elif register == CMP:
                self.alu("CMP", self.reg[operandA], self.reg[operandB])
                self.pc += 3
            
            elif register == JMP:
                reg_num = operandA
                destination = self.reg[reg_num]
                self.pc = destination

            elif register == JNE:
                if self.flag != 0b00000001:
                    reg_num = operandA
                    destination = self.reg[reg_num]
                    self.pc = destination
                else:
                    self.pc += 2

            elif register == JEQ:
                if self.flag == 0b00000001:
                    reg_num = operandA
                    destination = self.reg[reg_num]
                    self.pc = destination
                else:
                    self.pc += 2

                
