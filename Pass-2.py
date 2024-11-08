class AssemblerPass2:
    def __init__(self, intermediate_code, symbol_table, literal_table, mot):
        self.intermediate_code = intermediate_code
        self.symbol_table = symbol_table
        self.literal_table = literal_table
        self.mot = mot
        self.machine_code = []

    def generate_machine_code(self):
        for line in self.intermediate_code:
            loc_counter, label, opcode_info, operands = line
            
            if isinstance(opcode_info, tuple):
                opcode_type, opcode, length = opcode_info

                # Handling imperative statements (IS)
                if opcode_type == 'IS':
                    machine_instr = f"{opcode} "

                    # Handling operands
                    for operand in operands:
                        if operand in self.symbol_table:
                            machine_instr += f"{self.symbol_table[operand]} "
                        elif operand in self.literal_table:
                            machine_instr += f"{self.literal_table[operand]} "
                        elif operand in ['AREG', 'BREG', 'CREG', 'DREG']:
                            reg_code = {'AREG': '1', 'BREG': '2', 'CREG': '3', 'DREG': '4'}
                            machine_instr += f"{reg_code[operand]} "
                        else:
                            machine_instr += f"{operand} "

                    self.machine_code.append(f"{loc_counter}: {machine_instr.strip()}")

                # Handling declarative statements (DL)
                elif opcode_type == 'DL':
                    if opcode == '01':  # DC (Define Constant)
                        value = operands[0].strip("=‘’")
                        machine_instr = f"{value}"
                        self.machine_code.append(f"{loc_counter}: {machine_instr}")

                    elif opcode == '02':  # DS (Define Storage)
                        if operands[0].isdigit():  # Ensure it is numeric before converting
                            size = int(operands[0])
                            for i in range(size):
                                self.machine_code.append(f"{loc_counter + i}: 0")
                        else:
                            raise ValueError(f"Invalid operand for DS: {operands[0]}")

            # Handling assembly directives (AD) if required
            elif isinstance(opcode_info, str) and opcode_info == 'AD':
                continue  # In the second pass, we often skip assembler directives

    def write_output(self, filename):
        with open(filename, 'w') as file:
            file.write("Machine Code:\n")
            for line in self.machine_code:
                file.write(f"{line}\n")

    def assemble_pass2(self, output_file):
        self.generate_machine_code()
        self.write_output(output_file)

def parse_pass1_output(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    intermediate_code = []
    symbol_table = {}
    literal_table = {}
    section = None

    for line in lines:
        line = line.strip()
        if line == "Intermediate Code:":
            section = "intermediate_code"
        elif line == "Symbol Table:":
            section = "symbol_table"
        elif line == "Literal Table:":
            section = "literal_table"
        elif section == "intermediate_code":
            if line:
                loc_counter, label, opcode_info, operands = eval(line)
                intermediate_code.append((loc_counter, label, opcode_info, operands))
        elif section == "symbol_table":
            if line:
                symbol, address = line.split(": ")
                symbol_table[symbol] = int(address)
        elif section == "literal_table":
            if line:
                literal, address = line.split(": ")
                literal_table[literal] = int(address)

    return intermediate_code, symbol_table, literal_table

if __name__ == "__main__":
    mot = {
        'ORIGIN': ('AD','03',1),
        'STOP': ('IS', '00',1),
        'ADD': ('IS', '01',1),
        'SUB': ('IS', '02',1),
        'MULT': ('IS', '03',1),
        'MOVER': ('IS', '04',1),
        'MOVEM': ('IS', '05',1),
        'COMP': ('IS', '06',1),
        'BC': ('IS', '07',1),
        'DIV': ('IS', '08',1),
        'READ': ('IS', '09',1),
        'PRINT': ('IS', '10',1),
        'START': ('AD', '01',1),
        'END': ('AD', '02',1),            
        'EQU': ('AD', '04',1),
        'LTORG': ('AD', '05',1),
        'DC': ('DL', '01',1),
        'DS': ('DL', '02',1),
    }

    intermediate_code, symbol_table, literal_table = parse_pass1_output("output10.txt")
    assembler_pass2 = AssemblerPass2(intermediate_code, symbol_table, literal_table, mot)
    assembler_pass2.assemble_pass2("final_output.txt")
