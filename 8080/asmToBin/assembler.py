def asm_bin(filename):
    encoding = {
        "mov": ['01DS', 1],      # Move register to register
        "mvi": ['00D110', 2],    # Move immediate to register
        "lxi": ['00R0001', 3],  # Load register pair immediate
        "lda": ['00111010', 3],  # Load A from memory
        "sta": ['00110010', 3],  # Store A to memory
        "lhld": ['00101010', 3], # Load H:L from memory
        "shld": ['00100010', 3], # Store H:L to memory
        "ldax": ['00R1010', 1], # Load indirect through BC or DE
        "stax": ['00R0010', 1], # Store indirect through BC or DE
        "xchg": ['11101011', 1], # Exchange DE and HL content
        "add": ['10000S', 1],    # Add register to A
        "adi": ['11000110', 2],  # Add immediate to A
        "adc": ['10001S', 1],    # Add register to A with carry
        "aci": ['11001110', 2],  # Add immediate to A with carry
        "sub": ['10010S', 1],    # Subtract register from A
        "sui": ['11010110', 2],  # Subtract immediate from A
        "sbb": ['10011S', 1],    # Subtract register from A with borrow
        "sbi": ['11011110', 2],  # Subtract immediate from A with borrow
        "inr": ['00D100', 1],    # Increment register
        "dcr": ['00D101', 1],    # Decrement register
        "inx": ['00R0011', 1],  # Increment register pair
        "dcx": ['00R1011', 1],  # Decrement register pair
        "dad": ['00R1001', 1],  # Add register pair to HL
        "daa": ['00100111', 1],  # Decimal Adjust accumulator
        "ana": ['10100S', 1],    # AND register with A
        "ani": ['11100110', 2],  # AND immediate with A
        "ora": ['10110S', 1],    # OR register with A
        "ori": ['11110110', 2],  # OR immediate with A
        "xra": ['10101S', 1],    # Exclusive OR register with A
        "xri": ['11101110', 2],  # Exclusive OR immediate with A
        "cmp": ['10111S', 1],    # Compare register with A
        "cpi": ['11111110', 2],  # Compare immediate with A
        "rlc": ['00000111', 1],  # Rotate A left
        "rrc": ['00001111', 1],  # Rotate A right
        "ral": ['00010111', 1],  # Rotate A left through carry
        "rar": ['00011111', 1],  # Rotate A right through carry
        "cma": ['00101111', 1],  # Compliment A
        "cmc": ['00111111', 1],  # Compliment Carry flag
        "stc": ['00110111', 1],  # Set Carry flag
        "jmp": ['11000011', 3],  # Unconditional jump
        "jnz": ['11000010', 3],   # NZ (Z flag not set)
        "jz": ['11001010', 3],    # Z (Z flag set)
        "jnc": ['11010010', 3],   # NC (C flag not set)
        "jc": ['11011010', 3],    # C (C flag set)
        "jpo": ['11100010', 3],   # PO (P flag not set - ODD)
        "jpe": ['11101010', 3],   # PE (P flag set - EVEN)
        "jp": ['11110010', 3],    # P (S flag not set - POSITIVE)
        "jm": ['11111010', 3],    # M (S flag set - MINUS)
        "call": ['11001101', 3], # Unconditional subroutine call
        "cnz": ['11000100', 3],   # NZ (Z flag not set)
        "cz": ['11001100', 3],    # Z (Z flag set)
        "cnc": ['11010100', 3],   # NC (C flag not set)
        "cc": ['11011100', 3],    # C (C flag set)
        "cpo": ['11100100', 3],   # PO (P flag not set - ODD)
        "cpe": ['11101100', 3],   # PE (P flag set - EVEN)
        "cp": ['11110100', 3],    # P (S flag not set - POSITIVE)
        "cm": ['11111100', 3],    # M (S flag set - MINUS)
        "ret": ['11001001', 1],  # Unconditional return from subroutine
        "rnz": ['11000000', 1],   # NZ (Z flag not set)
        "rz": ['11001000', 1],    # Z (Z flag set)
        "rnc": ['11010000', 1],   # NC (C flag not set)
        "rc": ['11011000', 1],    # C (C flag set)
        "rpo": ['11100000', 1],   # PO (P flag not set - ODD)
        "rpe": ['11101000', 1],   # PE (P flag set - EVEN)
        "rp": ['11110000', 1],    # P (S flag not set - POSITIVE)
        "rm": ['11111000', 1],    # M (S flag set - MINUS)
        "rst": ['11N111', 1],    # Restart
        "pchl": ['11101001', 1], # Jump to address in H:L
        "push": ['11R0101', 1], # Push register pair on stack
        "pop": ['11R0001', 1],  # Pop register pair from stack
        "xthl": ['11100011', 1], # Swap H:L with top word on stack
        "sphl": ['11111001', 1], # Set SP to H:L
        "in": ['11011011', 2],   # Read input port into A
        "out": ['11010011', 2],  # Write A to output port
        "ei": ['11111011', 1],   # Enable interrupts
        "di": ['11110011', 1],   # Disable interrupts
        "hlt": ['01110110', 1],  # Halt processor
        "nop": ['00000000', 1],  # No operation
    }

    r_map = {
        'b': '000', 'c': '001', 'd': '010', 'e': '011',
        'h': '100', 'l': '101', 'm': '110', 'a': '111'
    }

    rp_map = {
        'b': '00', 'd': '01', 'h': '10', 'sp': '11',
        'bc': '00', 'de': '01', 'hl': '10', 'sp': '11'
    }

    bin = ''

    with open(filename, 'r') as file:
        mem_addr = 15
        loop = 0
        flag = 0
        for line in file:
            asm = line.replace(',', '').strip().split()
            n_in = len(asm)
            if asm[0] == 'loop:':
                flag = 1
                loop = mem_addr
            
            ins = encoding[asm[flag]][0]
            length = encoding[asm[flag]][1]
            
            if 'R' in ins:
                ins = ins.replace('R', rp_map[asm[flag + 1]])
            
            if 'D' in ins:
                if 'S' in ins:
                    ins = ins.replace('D', r_map[asm[flag + 1]])
                    ins = ins.replace('S', r_map[asm[flag + 2]])
                else:
                    ins = ins.replace('D', r_map[asm[flag + 1]])
            else:
                if 'S' in ins:
                    ins = ins.replace('S', r_map[asm[flag + 1]])

            bin += ins

            if asm[-1] == 'loop':
                addr = '{:016b}'.format(loop & 0xFFFF)
                bin += addr
            
            if asm[-1].isdigit():
                if (length - 1 == 1):
                    I = '{:08b}'.format(int(asm[-1]) & 0xFFFF)
                else:
                    I = '{:016b}'.format(int(asm[-1]) & 0xFFFF)
                bin += I

            mem_addr += encoding[asm[flag]][1]
            flag = 0

    with open("example.txt", "w") as filout:
        filout.write(bin)

asm_bin("./memcpy")
print()