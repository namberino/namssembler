import sys
import re
from opcode import opcodes_table

instructions = []

if len(sys.argv) <= 1:
	sys.exit("Usage: python asm85.py <file>.asm")
elif sys.argv[1][-4:] != ".asm":
	sys.exit("Invalid file extension! Please use '.asm'")

with open(sys.argv[1], "r") as f:
    for line in f:
        # skip empty lines
        if line == "\n" or line == "":
            continue
        
        # skip comments
        elif ";" in line:
            if line.index(";") == 0: # skip comment lines
                continue
            line = line[:line.index(";") - 1] # skip inline comments

        line = line.strip() # remove excess space

        instructions.append(line.rstrip('\n'))

# check is number is a valid 8085 hexadecimal
def is_hex(hex_num):
    if hex_num[-1] != "H":
        return False

    try:
        new_hex_num = int(hex_num[:-1], 16)
    except:
        return False
    
    return True

# try to convert number to int
def to_int(num):
    try:
        normal_num = int(num)
    except:
        normal_num = -1
    return normal_num

# remove the "H" from hex numbers (example: "25H" -> "25")
def normalize_hex(hex_num):
    hex_num = hex_num[:-1] # remove the "H"
    return hex_num

# search instructions in the opcode table
def search_instruction(lookup_instruction):
    opcode = opcodes_table[lookup_instruction]
    opcodef = hex(opcode)[2:]
    if len(opcodef) <= 1:
        opcodef = "0" + opcodef
    return opcodef

# add padding bytes to data
def pad_data(data):
    padding = "0" * (4 - len(data))

    data = padding + data
    MSB = data[:len(data) // 2]
    LSB = data[len(data) // 2:]
    
    return MSB, LSB

# find labels' locations
def labeling(split_instructions):
    labels = {}
    counter = 0

    for instruction in split_instructions:
        if instruction[0].endswith(":"):
            labels[instruction[0][:-1]] = hex(counter)
            continue
        
        if instruction[0] == ".ORG" and instruction[1].endswith("H"):
            counter += int(normalize_hex(instruction[1]), 16)
            continue

        if (instruction[0] == "ADC" or instruction[0] == "ADD" or instruction[0] == "ANA" or 
            instruction[0] == "CMA" or instruction[0] == "CMC" or instruction[0] == "CMP" or 
            instruction[0] == "DAA" or instruction[0] == "DAD" or instruction[0] == "ADI" or 
            instruction[0] == "DCR" or instruction[0] == "DCX" or instruction[0] == "DI" or 
            instruction[0] == "EI" or instruction[0] == "HLT" or instruction[0] == "INR" or 
            instruction[0] == "INX" or instruction[0] == "ADI" or instruction[0] == "LDAX" or
            instruction[0] == "MOV" or instruction[0] == "NOP" or instruction[0] == "ORA" or
            instruction[0] == "PCHL" or instruction[0] == "POP" or instruction[0] == "PUSH" or 
            instruction[0] == "RAL" or instruction[0] == "RAR" or instruction[0] == "RC" or 
            instruction[0] == "RET" or instruction[0] == "RIM" or instruction[0] == "RLC" or 
            instruction[0] == "RM" or instruction[0] == "RNZ" or instruction[0] == "RNC" or 
            instruction[0] == "RP" or instruction[0] == "RPE" or instruction[0] == "RPO" or 
            instruction[0] == "RRC" or instruction[0] == "RST" or instruction[0] == "RZ" or 
            instruction[0] == "SBB" or instruction[0] == "ADI" or instruction[0] == "SIM" or 
            instruction[0] == "SPHL" or instruction[0] == "STAX" or instruction[0] == "STC" or 
            instruction[0] == "SUB" or instruction[0] == "XCHG" or instruction[0] == "XRA" or 
            instruction[0] == "XTHL"):
            counter += 1
            continue

        if (instruction[0] == "ACI" or instruction[0] == "ADI" or instruction[0] == "ANI" or 
            instruction[0] == "CPI" or instruction[0] == "IN" or instruction[0] == "MVI" or 
            instruction[0] == "ORI" or instruction[0] == "OUT" or instruction[0] == "SBI" or
            instruction[0] == "SUI" or instruction[0] == "XRI"):
            counter += 2
            continue

        if (instruction[0] == "CALL" or instruction[0] == "CC" or instruction[0] == "CM" or 
            instruction[0] == "CNC" or instruction[0] == "CNZ" or instruction[0] == "CP" or
            instruction[0] == "CPE" or instruction[0] == "CPO" or instruction[0] == "CZ" or 
            instruction[0] == "ADI" or instruction[0] == "JC" or instruction[0] == "JM" or 
            instruction[0] == "JMP" or instruction[0] == "JNC" or instruction[0] == "JNZ" or 
            instruction[0] == "JP" or instruction[0] == "JPE" or instruction[0] == "JPO" or 
            instruction[0] == "JZ" or instruction[0] == "LDA" or instruction[0] == "LHLD" or 
            instruction[0] == "LXI" or instruction[0] == "SHLD" or instruction[0] == "STA"):
            counter += 3
            continue

    return labels

# main assembler function
def assembler(instructions):
    registers = "ABCDEHLM"
    split_instructions = []
    asm_bytes = []
    counter = 0x0

    for instruction in instructions:
        split_instructions.append(instruction.split(" "))

    labels = labeling(split_instructions)
    print(labels)

    for instruction in split_instructions:
        if instruction[0] == ".ORG":
            if not is_hex(instruction[1]):
                num = to_int(instruction[1])
                if num < 0:
                    print(f"Invalid padding number ({instruction[1]}) for '{instruction[0]}' on line {counter}")
                    return None
            
            num_of_padding = int(normalize_hex(instruction[1]), 16)

            while counter < num_of_padding:
                asm_bytes.append("00")
                counter += 1

        elif (instruction[0] == "ADC" or instruction[0] == "ADD" or instruction[0] == "ANA" or
              instruction[0] == "ORA" or instruction[0] == "POP" or instruction[0] == "PUSH" or
              instruction[0] == "RST" or instruction[0] == "SBB" or instruction[0] == "STAX" or
              instruction[0] == "SUB" or instruction[0] == "XRA" or instruction[0] == "LDAX" or
              instruction[0] == "CMP" or instruction[0] == "DCR" or instruction[0] == "INR" or
              instruction[0] == "DAD" or instruction[0] == "DCX" or instruction[0] == "INX"):
            if instruction[0] in ["ADC", "ADD", "ANA", "ORA", "SBB", "SUB", "XRA", "CMP", "DCR", "INR"]:
                if instruction[1] not in "ABCDEHLM":
                    print(f"Invalid register for '{instruction[0]}' on line {counter} (Use A, B, C, D, E, H, L, or M)")
                    return None
            
            if instruction[0] in ["POP", "PUSH"]:
                if instruction[1] not in ["B", "D", "H", "PSW"]:
                    print(f"Invalid register for '{instruction[0]}' on line {counter} (Use B, D, H, or PSW)")
                    return None

            if instruction[0] in ["STAX", "LDAX"]:
                if instruction[1] not in "BD":
                    print(f"Invalid register for '{instruction[0]}' on line {counter} (Use B or D)")
                    return None

            if instruction[0] == "RST":
                if instruction[1] < "0" or instruction[1] > "7":
                    print(f"Invalid reset mode for '{instruction[0]}' on line {counter} (Use 0 - 7)")
                    return None

            if instruction[0] in ["DAD", "DCX", "INX"]:
                if instruction[1] not in ["B", "D", "H", "SP"]:
                    print(f"Invalid register for '{instruction[0]}' on line {counter} (Use B, D, H, or SP)")
                    return None

            lookup_instruction = instruction[0] + " " + instruction[1]
            asm_bytes.append(search_instruction(lookup_instruction))
            counter += 1

        elif instruction[0] == "MOV":
            if instruction[1][:-1] not in "ABCDEHLM":
                print(f"Invalid destination register ({instruction[1]}) for '{instruction[0]}' on line {counter} (Use A, B, C, D, E, H, L, or M)")
                return None

            if instruction[2] not in "ABCDEHLM":
                print(f"Invalid source register ({instruction[2]}) for '{instruction[0]}' on line {counter} (Use A, B, C, D, E, H, L, or M)")
                return None

            lookup_instruction = instruction[0] + " " + instruction[1] + instruction[2]
            asm_bytes.append(search_instruction(lookup_instruction))
            counter += 1

        elif (instruction[0] == "PCHL" or instruction[0] == "RAL" or instruction[0] == "RAR" or
              instruction[0] == "RC" or instruction[0] == "RET" or instruction[0] == "RIM" or 
              instruction[0] == "RLC" or instruction[0] == "RM" or instruction[0] == "RNC" or 
              instruction[0] == "RNZ" or instruction[0] == "RP" or instruction[0] == "RPE" or 
              instruction[0] == "RPO" or instruction[0] == "RRC" or instruction[0] == "RZ" or 
              instruction[0] == "SIM" or instruction[0] == "SPHL" or instruction[0] == "STC" or
              instruction[0] == "XCHG" or instruction[0] == "XTHL" or instruction[0] == "CMA" or 
              instruction[0] == "CMC" or instruction[0] == "DAA" or instruction[0] == "DI" or 
              instruction[0] == "EI" or instruction[0] == "HLT"):
            lookup_instruction = instruction[0]
            asm_bytes.append(search_instruction(lookup_instruction))
            counter += 1

        elif instruction[0] == "NOP":
            asm_bytes.append("00")
            counter += 1

        elif (instruction[0] == "ACI" or instruction[0] == "ADI" or instruction[0] == "ANI" or
              instruction[0] == "ORI" or instruction[0] == "OUT" or instruction[0] == "IN" or
              instruction[0] == "SBI" or instruction[0] == "SUI" or instruction[0] == "XRI" or
              instruction[0] == "CPI"):
            if instruction[0] in ["ACI", "ADI", "ANI", "ORI", "SBI", "SUI", "XRI", "ACI"]:
                if not is_hex(instruction[1]):
                    print(f"Invalid data ({instruction[1]}) for '{instruction[0]}' on line {counter} (Use hexadecimal)")
                    return None

            if instruction[0] in ["OUT", "IN"]:
                if not is_hex(instruction[1]):
                    print(f"Invalid port address ({instruction[1]}) for '{instruction[0]}' on line {counter} (Use hexadecimal)")
                    return None
            
            lookup_instruction = instruction[0]
            asm_bytes.append(search_instruction(lookup_instruction))

            data = normalize_hex(instruction[1])
            asm_bytes.append("0" + data if len(data) <= 1 else data)
            counter += 2

        elif instruction[0] == "MVI" or instruction[0] == "LXI":
            if instruction[0] == "MVI":
                if instruction[1][:-1] not in "ABCDEHLM":
                    print(f"Invalid register ({instruction[1][:-1]}) for '{instruction[0]}' on line {counter} (Use A, B, C, D, E, H, L, or M)")
                    return None

            if instruction[0] == "LXI":
                if instruction[1][:-1] not in ["B", "D", "H", "SP"]:
                    print(f"Invalid register ({instruction[1][:-1]}) for '{instruction[0]}' on line {counter} (Use B, D, H, or SP)")
                    return None
                
            if not is_hex(instruction[2]):
                print(f"Invalid data ({instruction[2]}) for '{instruction[0]}' on line {counter} (Use hexadecimal)")
                return None

            lookup_instruction = instruction[0] + " " + instruction[1][:-1]
            asm_bytes.append(search_instruction(lookup_instruction))

            if instruction[0] == "MVI":
                data = normalize_hex(instruction[2])
                asm_bytes.append("0" + data if len(data) <= 1 else data)
                counter += 2
            elif instruction[0] == "LXI":
                data = normalize_hex(instruction[2])
                MSB, LSB = pad_data(data)
                
                asm_bytes.append(LSB)
                asm_bytes.append(MSB)
                counter += 3

        elif instruction[0] == "SHLD" or instruction[0] == "LHLD" or instruction[0] == "STA" or instruction[0] == "LDA":
            if not is_hex(instruction[1]):
                print(f"Invalid address ({instruction[1]}) for '{instruction[0]}' on line {counter} (Use hexadecimal)")
                return None

            lookup_instruction = instruction[0]
            asm_bytes.append(search_instruction(lookup_instruction))

            data = normalize_hex(instruction[1])
            MSB, LSB = pad_data(data)
            
            asm_bytes.append(LSB)
            asm_bytes.append(MSB)
            counter += 3

        elif (instruction[0] == "CALL" or instruction[0] == "CC" or instruction[0] == "CM" or 
              instruction[0] == "CNC" or instruction[0] == "CNZ" or instruction[0] == "CP" or 
              instruction[0] == "CPE" or instruction[0] == "CPO" or instruction[0] == "CZ" or
              instruction[0] == "JC" or instruction[0] == "JM" or instruction[0] == "JMP" or 
              instruction[0] == "JNC" or instruction[0] == "JNZ" or instruction[0] == "JP" or 
              instruction[0] == "JPE" or instruction[0] == "JPO" or instruction[0] == "JZ"):
            if instruction[1] not in labels:
                print(f"Invalid label ({instruction[1]}) for '{instruction[0]}' on line {counter} (Use hexadecimal)")
                return None
            
            lookup_instruction = instruction[0]
            asm_bytes.append(search_instruction(lookup_instruction))

            address = labels[instruction[1]]
            MSB, LSB = pad_data(address[2:])

            asm_bytes.append(LSB)
            asm_bytes.append(MSB)
            counter += 3

        elif instruction[0][:-1] in labels:
            counter += 1

        else:
            print(f"Invalid instruction ({instruction}) on line {counter} (Use 8085 instructions)")
            return None

    return asm_bytes


asm_bytes = assembler(instructions)
if asm_bytes != None:
    output_path = "out/" + sys.argv[1][4:-4] + ".bin"

    with open(output_path, "w") as f:
        for i in range(len(asm_bytes)):
            if i % 16 == 0 and i != 0:
                f.write("\n")
            f.write(asm_bytes[i])
            f.write(" ")

    print(f"Assembled program has been written to '{output_path}'")
