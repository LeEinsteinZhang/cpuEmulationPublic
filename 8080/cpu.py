# 8080 like cpu
# D   = Destination register (8 bit)
# S   = Source register (8 bit)
# RP  = Register pair (16 bit)
# I   = 8 or 16 bit immediate operand
# addr   = 16 bit Memory address
# port   = 8 bit port address
# ccc = Conditional

# 8-bit CPU 8080 like

EXIT_SUCESS = 1
EXIT_FAIL = 0
EXIT_ERROR = -1
NULL = [0,0,0,0,0,0,0,0]
HIGH = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
LOW = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

class CPU:
    def __init__(self, memory) -> None:
        self.mem = memory
        self.reg = [[0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # <- 0  F:[0...7] A:[8...15]   16-bits
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # <- 1  C:[0...7] B:[8...15]   16-bits
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # <- 2  E:[0...7] D:[8...15]   16-bits
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # <- 3  L:[0...7] H:[8...15]   16-bits
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # <- 4  SP:[0...15]            16-bits
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # <- 5  PC:[0...15]            16-bits
                #    ^  ^  ^  ^  ^  ^  ^  ^  ^  ^  ^  ^  ^  ^  ^  ^
                #    00,01,02,03,04,05,06,07,08,09,10,11,12,13,14,15
                    ]
        
    def reg_reader(self, num, start, end):
        result = []
        for i in range(start, end + 1):
            result.append(self.reg[num][i])
        return result

    def reg_writer(self, num, start, end, data):
        data_size = len(data)
        dest_size = end - start + 1
        if data_size > dest_size:
            return EXIT_ERROR
        else:
            for i in range(dest_size):
                if i < data_size:
                    self.reg[num][start + i] = data[i]
                else:
                    self.reg[num][start + i] = 0
            return EXIT_SUCESS

    def reg_r(self, reg):
        if reg == 'A':
            return self.reg_reader(0,8,15)
        elif reg == 'F':
            return self.reg_reader(0, 0, 7)
        elif reg == 'B':
            return self.reg_reader(1,8,15)
        elif reg == 'C':
            return self.reg_reader(1,0,7)
        elif reg == 'D':
            return self.reg_reader(2,8,15)
        elif reg == 'E':
            return self.reg_reader(2,0,7)
        elif reg == 'H':
            return self.reg_reader(3,8,15)
        elif reg == 'L':
            return self.reg_reader(3,0,7)
        elif reg == 'BC':
            return self.reg_reader(1,0,15)
        elif reg == 'DE':
            return self.reg_reader(2,0,15)
        elif reg == 'HL' or reg == 'M':
            return self.reg_reader(3,0,15)
        elif reg == 'SP':
            return self.reg_reader(4,0,15)
        elif reg == 'PC':
            return self.reg_reader(5,0,15)
        else:
            return EXIT_ERROR

    def reg_w(self, reg, data):
        if reg == 'A':
            self.reg_writer(0,8,15,data)
        elif reg == 'F':
            self.reg_writer(0, 0, 7,data)
        elif reg == 'B':
            self.reg_writer(1,8,15,data)
        elif reg == 'C':
            self.reg_writer(1,0,7,data)
        elif reg == 'D':
            self.reg_writer(2,8,15,data)
        elif reg == 'E':
            self.reg_writer(2,0,7,data)
        elif reg == 'H':
            self.reg_writer(3,8,15,data)
        elif reg == 'L':
            self.reg_writer(3,0,7,data)
        elif reg == 'BC':
            self.reg_writer(1,0,15,data)
        elif reg == 'DE':
            self.reg_writer(2,0,15,data)
        elif reg == 'HL' or reg == 'M':
            self.reg_writer(3,0,15,data)
        elif reg == 'SP':
            self.reg_writer(4,0,15,data)
        elif reg == 'PC':
            self.reg_writer(5,0,15,data)
        else:
            return EXIT_ERROR

    def set_C(self):
        self.reg[0][0] = 1

    def get_C(self):
        return self.reg[0][0]

    def set_P(self):
        self.reg[0][2] = 1

    def get_P(self):
        return self.reg[0][2]
    def set_A(self):
        self.reg[0][4] = 1

    def get_A(self):
        return self.reg[0][4]

    def set_Z(self):
        self.reg[0][6] = 1

    def get_Z(self):
        return self.reg[0][6]
    def set_S(self):
        self.reg[0][7] = 1

    def get_S(self):
        return self.reg[0][7]

    def int_to_bits_8b(self, value):
        if value < 0:
            self.reset_flags()
            self.set_S()
        return [int(bit) for bit in '{:08b}'.format(value & 0xFF)]

    def int_to_bits_16b(self, value):
        if value < 0:
            self.set_S()
        return [int(bit) for bit in '{:016b}'.format(value & 0xFFFF)]

    def reset_flags(self):
        self.reg[0][0] = 0
        self.reg[0][2] = 0
        self.reg[0][4] = 0
        self.reg[0][6] = 0
        self.reg[0][7] = 0

    def bits_to_int(self, bits):
        return int(''.join(str(bit) for bit in bits), 2)

    def adder(self, v1, v2):
        size = len(v1)
        result = []
        carry = 0
        for i in range(size):
            bit1 = v1[-(i + 1)] if i < size else 0
            bit2 = v2[-(i + 1)] if i < size else 0
            total = bit1 + bit2 + carry
            result_bit = total % 2
            carry = total // 2
            result.insert(0, result_bit)
        if carry != 0:
            result.insert(0, carry)
        return result
    
    def two_complement(self, binary_number):
        one_complement = [1 if bit == 0 else 0 for bit in binary_number]
        return self.adder(one_complement, [0] * (len(binary_number) - 1) + [1])

    def subtractor(self, v1, v2):
        twos_complement_v2 = self.two_complement(v2)
        result = self.adder(v1, twos_complement_v2)
        if len(result) > len(v1):
            result = result[1:]
        return result

    def mov(self, D, S):
        if D == 'M':
            self.mem.io(1, self.reg_r(D), self.reg_r(S))
        else:
            self.reg_w(D, self.reg_r(S))
            return EXIT_SUCESS

    def mvi(self, D, I):
        self.reg_w(D, I)
        return EXIT_SUCESS

    def lxi(self, RP, I):
        self.reg_w(RP, I)

    def lda(self, addr):
        self.reg_w('A', self.mem.io(0, addr))
        return EXIT_SUCESS

    def sta(self, addr):
        self.mem.io(1, addr, self.reg_r('A'))
        return EXIT_SUCESS

    def lhld(self, addr):
        addr_1 = self.adder(addr, self.int_to_bits_16b(1))
        self.reg_w('HL', self.mem.io(0,addr) + self.mem.io(0,addr_1))

    def shld(self, addr):
        addr_1 = self.adder(addr, self.int_to_bits_16b(1))
        self.mem.io(1, addr, self.reg_r('HL')[:8])
        self.mem.io(1, addr_1, self.reg_r('HL')[8:])

    def ldax(self, RP):
        addr = self.reg_r(RP)
        self.lda(addr)

    def stax(self, RP):
        addr = self.reg_r(RP)
        self.sta(addr)

    def xchg(self):
        for i in range(16):
            self.reg[2][i] = self.reg[2][i] ^ self.reg[3][i]
            self.reg[3][i] = self.reg[2][i] ^ self.reg[3][i]
            self.reg[2][i] = self.reg[2][i] ^ self.reg[3][i]

    def add(self, S):
        val = self.reg_r(S)
        val_A = self.reg_r('A')
        self.reg_w('A', self.adder(val, val_A))
        return EXIT_SUCESS

    def adi(self, I):
        val_A = self.reg_r('A')
        self.reg_w('A', self.adder(val_A, I))
        return EXIT_SUCESS

    def adc(self, S):
        pass

    def aci(self, I):
        pass

    def sub(self, S):
        val_A = self.reg_r('A')
        val = self.reg_r(S)
        self.reg_w('A', self.subtractor(val_A, val))
        return EXIT_SUCESS

    def sui(self, I):
        val = self.int_to_bits_8b(I)
        val_A = self.reg_r('A')
        self.reg_w('A', self.subtractor(val_A, val))
        return EXIT_SUCESS

    def sbb(self, S):
        pass

    def sbi(self, I):
        pass

    def inr(self, D):
        self.reg_w(D, self.adder(self.reg_r(D), self.int_to_bits_8b(1)))

    def dcr(self, D):
        self.reg_w(D, self.subtractor(self.reg_r(D), self.int_to_bits_8b(1)))

    def inx(self, RP):
        self.reg_w(RP, self.adder(self.reg_r(RP), self.int_to_bits_16b(1)))

    def dcx(self, RP):
        self.reg_w(RP, self.subtractor(self.reg_r(RP), self.int_to_bits_16b(1)))

    def dad(self, RP):
        self.reg_w('HL', self.adder(self.reg_r('HL'), self.reg_r(RP)))

    def daa(self):
        pass

    def ana(self, S):
        for i in range(8):
            self.reg[0][8+i] = self.reg[0][8+i] and self.reg_r(S)[i]

    def ani(self, I):
        for i in range(8):
            self.reg[0][8+i] = self.reg[0][8+i] and I[i]

    def ora(self, S):
        for i in range(8):
            self.reg[0][8+i] = self.reg[0][8+i] or self.reg_r(S)[i]
        if not self.bits_to_int(self.reg_r('A')):
            self.set_Z()

    def ori(self, I):
        for i in range(8):
            self.reg[0][8+i] = self.reg[0][8+i] or I[i]

    def xra(self, S):
        for i in range(8):
            self.reg[0][8+i] = self.reg[0][8+i] ^ self.reg_r(S)[i]

    def xri(self, I):
        for i in range(8):
            self.reg[0][8+i] = self.reg[0][8+i] ^ I[i]

    def cmp(self, S):
        pass

    def cpi(self, I):
        pass

    def rlc(self):
        pass

    def rrc(self):
        pass

    def ral(self):
        pass

    def rar(self):
        pass

    def cma(self):
        self.reg_w('A', [1 if bit == 0 else 0 for bit in self.reg_r('A')])

    def cmc(self):
        self.reg[0][0] = not self.reg[0][0]

    def stc(self):
        self.set_C()

    def jmp(self, addr):
        self.reg_w('PC', addr)
        self.dcx('PC')

    def jccc(self, addr, ccc):
        pass

    def call(self, addr):
        pass

    def cccc(self, addr, ccc):
        pass

    def ret(self):
        return EXIT_SUCESS

    def rccc(self, ccc):
        pass

    def rst(self, n):
        pass

    def pchl(self):
        self.jmp(self.reg_r('HL'))

    def push(self, RP):
        # Always split the data into lower and higher bytes
        data = self.reg_r(RP)
        lb = data[:8]
        hb = data[8:]
        # Push higher byte and then lower byte onto the stack
        self.dcx('SP')
        self.mem.io(1, self.reg_r('SP'), hb)
        self.dcx('SP')
        self.mem.io(1, self.reg_r('SP'), lb)

    def pop(self, RP):
        if self.reg_r('SP') == HIGH:
            print("EMPTY STACK")
        else:
            lb = self.mem.io(0, self.reg_r('SP'))
            self.inx('SP')
            hb = self.mem.io(0, self.reg_r('SP'))
            self.inx('SP')
            data = lb + hb
            self.reg_w(RP, data)

    def xthl(self):
        lb = self.reg_r('L')
        hb = self.reg_r('H')
        self.reg_w('L',self.mem.io(0,self.reg_r('SP')))
        self.mem.io(1,self.reg_r('SP'),lb)
        self.inx('SP')
        self.reg_w('H',self.mem.io(0,self.reg_r('SP')))
        self.mem.io(1,self.reg_r('SP'),hb)
        self.dcx('SP')

    def sphl(self):
        pass

    def _in(self, byte):
        pass

    def _out(self, byte):
        pass

    def ei(self):
        pass

    def di(self):
        pass

    def hlt(self):
        pass

    def nop(self):
        return 0
    
    #################################################################################
    #
    # BELOW IS THE CPU EXECTUTION
    #
    #################################################################################

    def RESET(self):
        pass

    def fetch(self):
        instruction = self.mem.io(0,self.reg_r('PC'))
        return instruction

    def execute(self, instruction):
        if instruction == [0, 0, 0, 0, 0, 0, 0, 0]:
            self.nop()

        elif instruction == [0, 0, 0, 0, 0, 0, 0, 1]:
            self.inx('PC')
            lb = self.mem.io(0, self.reg_r('PC'))
            self.inx('PC')
            hb = self.mem.io(0, self.reg_r('PC'))
            data = lb + hb
            self.lxi('BC', data)

        elif instruction == [0, 0, 0, 0, 0, 0, 1, 0]:
            self.stax('BC')

        elif instruction == [0, 0, 0, 0, 0, 0, 1, 1]:
            self.inx('BC')

        elif instruction == [0, 0, 0, 0, 0, 1, 0, 0]:
            self.inr('B')

        elif instruction == [0, 0, 0, 0, 0, 1, 0, 1]:
            self.dcr('B')

        elif instruction == [0, 0, 0, 0, 0, 1, 1, 0]:
            self.inx('PC')
            data = self.mem.io(0, self.reg_r('PC'))
            self.mvi('B', data)

        elif instruction == [0, 0, 0, 0, 0, 1, 1, 1]:
            self.rlc()

        elif instruction == [0, 0, 0, 0, 1, 0, 0, 0]:
            self.nop()

        elif instruction == [0, 0, 0, 0, 1, 0, 0, 1]:
            self.dad('BC')

        elif instruction == [0, 0, 0, 0, 1, 0, 1, 0]:
            self.ldax('BC')

        elif instruction == [0, 0, 0, 0, 1, 0, 1, 1]:
            self.dcx('BC')

        elif instruction == [0, 0, 0, 0, 1, 1, 0, 0]:
            self.inr('C')

        elif instruction == [0, 0, 0, 0, 1, 1, 0, 1]:
            self.dcr('C')

        elif instruction == [0, 0, 0, 0, 1, 1, 1, 0]:
            self.inx('PC')
            data = self.mem.io(0, self.reg_r('PC'))
            self.mvi('C', data)

        elif instruction == [0, 0, 0, 0, 1, 1, 1, 1]:
            self.rrc()

        elif instruction == [0, 0, 0, 1, 0, 0, 0, 0]:
            pass
            # Execute the operation for 00010000
        elif instruction == [0, 0, 0, 1, 0, 0, 0, 1]:
            pass
            # Execute the operation for 00010001
        elif instruction == [0, 0, 0, 1, 0, 0, 1, 0]:
            pass
            # Execute the operation for 00010010
        elif instruction == [0, 0, 0, 1, 0, 0, 1, 1]:
            self.inx('DE')

        elif instruction == [0, 0, 0, 1, 0, 1, 0, 0]:
            pass
            # Execute the operation for 00010100
        elif instruction == [0, 0, 0, 1, 0, 1, 0, 1]:
            pass
            # Execute the operation for 00010101
        elif instruction == [0, 0, 0, 1, 0, 1, 1, 0]:
            pass
            # Execute the operation for 00010110
        elif instruction == [0, 0, 0, 1, 0, 1, 1, 1]:
            pass
            # Execute the operation for 00010111
        elif instruction == [0, 0, 0, 1, 1, 0, 0, 0]:
            pass
            # Execute the operation for 00011000
        elif instruction == [0, 0, 0, 1, 1, 0, 0, 1]:
            pass
            # Execute the operation for 00011001
        elif instruction == [0, 0, 0, 1, 1, 0, 1, 0]:
            self.ldax('DE')

        elif instruction == [0, 0, 0, 1, 1, 0, 1, 1]:
            pass
            # Execute the operation for 00011011
        elif instruction == [0, 0, 0, 1, 1, 1, 0, 0]:
            pass
            # Execute the operation for 00011100
        elif instruction == [0, 0, 0, 1, 1, 1, 0, 1]:
            pass
            # Execute the operation for 00011101
        elif instruction == [0, 0, 0, 1, 1, 1, 1, 0]:
            pass
            # Execute the operation for 00011110
        elif instruction == [0, 0, 0, 1, 1, 1, 1, 1]:
            pass
            # Execute the operation for 00011111
        elif instruction == [0, 0, 1, 0, 0, 0, 0, 0]:
            pass
            # Execute the operation for 00100000
        elif instruction == [0, 0, 1, 0, 0, 0, 0, 1]:
            self.inx('PC')
            lb = self.mem.io(0, self.reg_r('PC'))
            self.inx('PC')
            hb = self.mem.io(0, self.reg_r('PC'))
            I = lb + hb
            self.lxi('HL', I)

        elif instruction == [0, 0, 1, 0, 0, 0, 1, 0]:
            pass
            # Execute the operation for 00100010
        elif instruction == [0, 0, 1, 0, 0, 0, 1, 1]:
            self.inx('HL')

        elif instruction == [0, 0, 1, 0, 0, 1, 0, 0]:
            pass
            # Execute the operation for 00100100
        elif instruction == [0, 0, 1, 0, 0, 1, 0, 1]:
            pass
            # Execute the operation for 00100101
        elif instruction == [0, 0, 1, 0, 0, 1, 1, 0]:
            pass
            # Execute the operation for 00100110
        elif instruction == [0, 0, 1, 0, 0, 1, 1, 1]:
            pass
            # Execute the operation for 00100111
        elif instruction == [0, 0, 1, 0, 1, 0, 0, 0]:
            pass
            # Execute the operation for 00101000
        elif instruction == [0, 0, 1, 0, 1, 0, 0, 1]:
            pass
            # Execute the operation for 00101001
        elif instruction == [0, 0, 1, 0, 1, 0, 1, 0]:
            pass
            # Execute the operation for 00101010
        elif instruction == [0, 0, 1, 0, 1, 0, 1, 1]:
            pass
            # Execute the operation for 00101011
        elif instruction == [0, 0, 1, 0, 1, 1, 0, 0]:
            pass
            # Execute the operation for 00101100
        elif instruction == [0, 0, 1, 0, 1, 1, 0, 1]:
            pass
            # Execute the operation for 00101101
        elif instruction == [0, 0, 1, 0, 1, 1, 1, 0]:
            pass
            # Execute the operation for 00101110
        elif instruction == [0, 0, 1, 0, 1, 1, 1, 1]:
            pass
            # Execute the operation for 00101111
        elif instruction == [0, 0, 1, 1, 0, 0, 0, 0]:
            pass
            # Execute the operation for 00110000
        elif instruction == [0, 0, 1, 1, 0, 0, 0, 1]:
            self.inx('PC')
            lb = self.mem.io(0, self.reg_r('PC'))
            self.inx('PC')
            hb = self.mem.io(0, self.reg_r('PC'))
            I = lb + hb
            self.lxi('SP', I)

        elif instruction == [0, 0, 1, 1, 0, 0, 1, 0]:
            pass
            # Execute the operation for 00110010
        elif instruction == [0, 0, 1, 1, 0, 0, 1, 1]:
            pass
            # Execute the operation for 00110011
        elif instruction == [0, 0, 1, 1, 0, 1, 0, 0]:
            pass
            # Execute the operation for 00110100
        elif instruction == [0, 0, 1, 1, 0, 1, 0, 1]:
            pass
            # Execute the operation for 00110101
        elif instruction == [0, 0, 1, 1, 0, 1, 1, 0]:
            pass
            # Execute the operation for 00110110
        elif instruction == [0, 0, 1, 1, 0, 1, 1, 1]:
            pass
            # Execute the operation for 00110111
        elif instruction == [0, 0, 1, 1, 1, 0, 0, 0]:
            pass
            # Execute the operation for 00111000
        elif instruction == [0, 0, 1, 1, 1, 0, 0, 1]:
            pass
            # Execute the operation for 00111001
        elif instruction == [0, 0, 1, 1, 1, 0, 1, 0]:
            pass
            # Execute the operation for 00111010
        elif instruction == [0, 0, 1, 1, 1, 0, 1, 1]:
            pass
            # Execute the operation for 00111011
        elif instruction == [0, 0, 1, 1, 1, 1, 0, 0]:
            pass
            # Execute the operation for 00111100
        elif instruction == [0, 0, 1, 1, 1, 1, 0, 1]:
            pass
            # Execute the operation for 00111101
        elif instruction == [0, 0, 1, 1, 1, 1, 1, 0]:
            pass
            # Execute the operation for 00111110
        elif instruction == [0, 0, 1, 1, 1, 1, 1, 1]:
            pass
            # Execute the operation for 00111111
        elif instruction == [0, 1, 0, 0, 0, 0, 0, 0]:
            pass
            # Execute the operation for 01000000
        elif instruction == [0, 1, 0, 0, 0, 0, 0, 1]:
            pass
            # Execute the operation for 01000001
        elif instruction == [0, 1, 0, 0, 0, 0, 1, 0]:
            pass
            # Execute the operation for 01000010
        elif instruction == [0, 1, 0, 0, 0, 0, 1, 1]:
            pass
            # Execute the operation for 01000011
        elif instruction == [0, 1, 0, 0, 0, 1, 0, 0]:
            pass
            # Execute the operation for 01000100
        elif instruction == [0, 1, 0, 0, 0, 1, 0, 1]:
            pass
            # Execute the operation for 01000101
        elif instruction == [0, 1, 0, 0, 0, 1, 1, 0]:
            pass
            # Execute the operation for 01000110
        elif instruction == [0, 1, 0, 0, 0, 1, 1, 1]:
            pass
            # Execute the operation for 01000111
        elif instruction == [0, 1, 0, 0, 1, 0, 0, 0]:
            pass
            # Execute the operation for 01001000
        elif instruction == [0, 1, 0, 0, 1, 0, 0, 1]:
            pass
            # Execute the operation for 01001001
        elif instruction == [0, 1, 0, 0, 1, 0, 1, 0]:
            pass
            # Execute the operation for 01001010
        elif instruction == [0, 1, 0, 0, 1, 0, 1, 1]:
            pass
            # Execute the operation for 01001011
        elif instruction == [0, 1, 0, 0, 1, 1, 0, 0]:
            pass
            # Execute the operation for 01001100
        elif instruction == [0, 1, 0, 0, 1, 1, 0, 1]:
            pass
            # Execute the operation for 01001101
        elif instruction == [0, 1, 0, 0, 1, 1, 1, 0]:
            pass
            # Execute the operation for 01001110
        elif instruction == [0, 1, 0, 0, 1, 1, 1, 1]:
            pass
            # Execute the operation for 01001111
        elif instruction == [0, 1, 0, 1, 0, 0, 0, 0]:
            pass
            # Execute the operation for 01010000
        elif instruction == [0, 1, 0, 1, 0, 0, 0, 1]:
            pass
            # Execute the operation for 01010001
        elif instruction == [0, 1, 0, 1, 0, 0, 1, 0]:
            pass
            # Execute the operation for 01010010
        elif instruction == [0, 1, 0, 1, 0, 0, 1, 1]:
            pass
            # Execute the operation for 01010011
        elif instruction == [0, 1, 0, 1, 0, 1, 0, 0]:
            pass
            # Execute the operation for 01010100
        elif instruction == [0, 1, 0, 1, 0, 1, 0, 1]:
            pass
            # Execute the operation for 01010101
        elif instruction == [0, 1, 0, 1, 0, 1, 1, 0]:
            pass
            # Execute the operation for 01010110
        elif instruction == [0, 1, 0, 1, 0, 1, 1, 1]:
            pass
            # Execute the operation for 01010111
        elif instruction == [0, 1, 0, 1, 1, 0, 0, 0]:
            pass
            # Execute the operation for 01011000
        elif instruction == [0, 1, 0, 1, 1, 0, 0, 1]:
            pass
            # Execute the operation for 01011001
        elif instruction == [0, 1, 0, 1, 1, 0, 1, 0]:
            pass
            # Execute the operation for 01011010
        elif instruction == [0, 1, 0, 1, 1, 0, 1, 1]:
            pass
            # Execute the operation for 01011011
        elif instruction == [0, 1, 0, 1, 1, 1, 0, 0]:
            pass
            # Execute the operation for 01011100
        elif instruction == [0, 1, 0, 1, 1, 1, 0, 1]:
            pass
            # Execute the operation for 01011101
        elif instruction == [0, 1, 0, 1, 1, 1, 1, 0]:
            pass
            # Execute the operation for 01011110
        elif instruction == [0, 1, 0, 1, 1, 1, 1, 1]:
            pass
            # Execute the operation for 01011111
        elif instruction == [0, 1, 1, 0, 0, 0, 0, 0]:
            pass
            # Execute the operation for 01100000
        elif instruction == [0, 1, 1, 0, 0, 0, 0, 1]:
            pass
            # Execute the operation for 01100001
        elif instruction == [0, 1, 1, 0, 0, 0, 1, 0]:
            pass
            # Execute the operation for 01100010
        elif instruction == [0, 1, 1, 0, 0, 0, 1, 1]:
            pass
            # Execute the operation for 01100011
        elif instruction == [0, 1, 1, 0, 0, 1, 0, 0]:
            pass
            # Execute the operation for 01100100
        elif instruction == [0, 1, 1, 0, 0, 1, 0, 1]:
            pass
            # Execute the operation for 01100101
        elif instruction == [0, 1, 1, 0, 0, 1, 1, 0]:
            pass
            # Execute the operation for 01100110
        elif instruction == [0, 1, 1, 0, 0, 1, 1, 1]:
            pass
            # Execute the operation for 01100111
        elif instruction == [0, 1, 1, 0, 1, 0, 0, 0]:
            pass
            # Execute the operation for 01101000
        elif instruction == [0, 1, 1, 0, 1, 0, 0, 1]:
            pass
            # Execute the operation for 01101001
        elif instruction == [0, 1, 1, 0, 1, 0, 1, 0]:
            pass
            # Execute the operation for 01101010
        elif instruction == [0, 1, 1, 0, 1, 0, 1, 1]:
            pass
            # Execute the operation for 01101011
        elif instruction == [0, 1, 1, 0, 1, 1, 0, 0]:
            pass
            # Execute the operation for 01101100
        elif instruction == [0, 1, 1, 0, 1, 1, 0, 1]:
            pass
            # Execute the operation for 01101101
        elif instruction == [0, 1, 1, 0, 1, 1, 1, 0]:
            pass
            # Execute the operation for 01101110
        elif instruction == [0, 1, 1, 0, 1, 1, 1, 1]:
            pass
            # Execute the operation for 01101111
        elif instruction == [0, 1, 1, 1, 0, 0, 0, 0]:
            pass
            # Execute the operation for 01110000
        elif instruction == [0, 1, 1, 1, 0, 0, 0, 1]:
            pass
            # Execute the operation for 01110001
        elif instruction == [0, 1, 1, 1, 0, 0, 1, 0]:
            pass
            # Execute the operation for 01110010
        elif instruction == [0, 1, 1, 1, 0, 0, 1, 1]:
            pass
            # Execute the operation for 01110011
        elif instruction == [0, 1, 1, 1, 0, 1, 0, 0]:
            pass
            # Execute the operation for 01110100
        elif instruction == [0, 1, 1, 1, 0, 1, 0, 1]:
            pass
            # Execute the operation for 01110101
        elif instruction == [0, 1, 1, 1, 0, 1, 1, 0]:
            pass
            # Execute the operation for 01110110
        elif instruction == [0, 1, 1, 1, 0, 1, 1, 1]:
            self.mov('M', 'A')

        elif instruction == [0, 1, 1, 1, 1, 0, 0, 0]:
            self.mov('A', 'B')

        elif instruction == [0, 1, 1, 1, 1, 0, 0, 1]:
            pass
            # Execute the operation for 01111001
        elif instruction == [0, 1, 1, 1, 1, 0, 1, 0]:
            pass
            # Execute the operation for 01111010
        elif instruction == [0, 1, 1, 1, 1, 0, 1, 1]:
            pass
            # Execute the operation for 01111011
        elif instruction == [0, 1, 1, 1, 1, 1, 0, 0]:
            pass
            # Execute the operation for 01111100
        elif instruction == [0, 1, 1, 1, 1, 1, 0, 1]:
            pass
            # Execute the operation for 01111101
        elif instruction == [0, 1, 1, 1, 1, 1, 1, 0]:
            pass
            # Execute the operation for 01111110
        elif instruction == [0, 1, 1, 1, 1, 1, 1, 1]:
            pass
            # Execute the operation for 01111111
        elif instruction == [1, 0, 0, 0, 0, 0, 0, 0]:
            pass
            # Execute the operation for 10000000
        elif instruction == [1, 0, 0, 0, 0, 0, 0, 1]:
            pass
            # Execute the operation for 10000001
        elif instruction == [1, 0, 0, 0, 0, 0, 1, 0]:
            pass
            # Execute the operation for 10000010
        elif instruction == [1, 0, 0, 0, 0, 0, 1, 1]:
            pass
            # Execute the operation for 10000011
        elif instruction == [1, 0, 0, 0, 0, 1, 0, 0]:
            pass
            # Execute the operation for 10000100
        elif instruction == [1, 0, 0, 0, 0, 1, 0, 1]:
            pass
            # Execute the operation for 10000101
        elif instruction == [1, 0, 0, 0, 0, 1, 1, 0]:
            pass
            # Execute the operation for 10000110
        elif instruction == [1, 0, 0, 0, 0, 1, 1, 1]:
            pass
            # Execute the operation for 10000111
        elif instruction == [1, 0, 0, 0, 1, 0, 0, 0]:
            pass
            # Execute the operation for 10001000
        elif instruction == [1, 0, 0, 0, 1, 0, 0, 1]:
            pass
            # Execute the operation for 10001001
        elif instruction == [1, 0, 0, 0, 1, 0, 1, 0]:
            pass
            # Execute the operation for 10001010
        elif instruction == [1, 0, 0, 0, 1, 0, 1, 1]:
            pass
            # Execute the operation for 10001011
        elif instruction == [1, 0, 0, 0, 1, 1, 0, 0]:
            pass
            # Execute the operation for 10001100
        elif instruction == [1, 0, 0, 0, 1, 1, 0, 1]:
            pass
            # Execute the operation for 10001101
        elif instruction == [1, 0, 0, 0, 1, 1, 1, 0]:
            pass
            # Execute the operation for 10001110
        elif instruction == [1, 0, 0, 0, 1, 1, 1, 1]:
            pass
            # Execute the operation for 10001111
        elif instruction == [1, 0, 0, 1, 0, 0, 0, 0]:
            pass
            # Execute the operation for 10010000
        elif instruction == [1, 0, 0, 1, 0, 0, 0, 1]:
            pass
            # Execute the operation for 10010001
        elif instruction == [1, 0, 0, 1, 0, 0, 1, 0]:
            pass
            # Execute the operation for 10010010
        elif instruction == [1, 0, 0, 1, 0, 0, 1, 1]:
            pass
            # Execute the operation for 10010011
        elif instruction == [1, 0, 0, 1, 0, 1, 0, 0]:
            pass
            # Execute the operation for 10010100
        elif instruction == [1, 0, 0, 1, 0, 1, 0, 1]:
            pass
            # Execute the operation for 10010101
        elif instruction == [1, 0, 0, 1, 0, 1, 1, 0]:
            pass
            # Execute the operation for 10010110
        elif instruction == [1, 0, 0, 1, 0, 1, 1, 1]:
            pass
            # Execute the operation for 10010111
        elif instruction == [1, 0, 0, 1, 1, 0, 0, 0]:
            pass
            # Execute the operation for 10011000
        elif instruction == [1, 0, 0, 1, 1, 0, 0, 1]:
            pass
            # Execute the operation for 10011001
        elif instruction == [1, 0, 0, 1, 1, 0, 1, 0]:
            pass
            # Execute the operation for 10011010
        elif instruction == [1, 0, 0, 1, 1, 0, 1, 1]:
            pass
            # Execute the operation for 10011011
        elif instruction == [1, 0, 0, 1, 1, 1, 0, 0]:
            pass
            # Execute the operation for 10011100
        elif instruction == [1, 0, 0, 1, 1, 1, 0, 1]:
            pass
            # Execute the operation for 10011101
        elif instruction == [1, 0, 0, 1, 1, 1, 1, 0]:
            pass
            # Execute the operation for 10011110
        elif instruction == [1, 0, 0, 1, 1, 1, 1, 1]:
            pass
            # Execute the operation for 10011111
        elif instruction == [1, 0, 1, 0, 0, 0, 0, 0]:
            pass
            # Execute the operation for 10100000
        elif instruction == [1, 0, 1, 0, 0, 0, 0, 1]:
            pass
            # Execute the operation for 10100001
        elif instruction == [1, 0, 1, 0, 0, 0, 1, 0]:
            pass
            # Execute the operation for 10100010
        elif instruction == [1, 0, 1, 0, 0, 0, 1, 1]:
            pass
            # Execute the operation for 10100011
        elif instruction == [1, 0, 1, 0, 0, 1, 0, 0]:
            pass
            # Execute the operation for 10100100
        elif instruction == [1, 0, 1, 0, 0, 1, 0, 1]:
            pass
            # Execute the operation for 10100101
        elif instruction == [1, 0, 1, 0, 0, 1, 1, 0]:
            pass
            # Execute the operation for 10100110
        elif instruction == [1, 0, 1, 0, 0, 1, 1, 1]:
            pass
            # Execute the operation for 10100111
        elif instruction == [1, 0, 1, 0, 1, 0, 0, 0]:
            pass
            # Execute the operation for 10101000
        elif instruction == [1, 0, 1, 0, 1, 0, 0, 1]:
            pass
            # Execute the operation for 10101001
        elif instruction == [1, 0, 1, 0, 1, 0, 1, 0]:
            pass
            # Execute the operation for 10101010
        elif instruction == [1, 0, 1, 0, 1, 0, 1, 1]:
            pass
            # Execute the operation for 10101011
        elif instruction == [1, 0, 1, 0, 1, 1, 0, 0]:
            pass
            # Execute the operation for 10101100
        elif instruction == [1, 0, 1, 0, 1, 1, 0, 1]:
            pass
            # Execute the operation for 10101101
        elif instruction == [1, 0, 1, 0, 1, 1, 1, 0]:
            pass
            # Execute the operation for 10101110
        elif instruction == [1, 0, 1, 0, 1, 1, 1, 1]:
            pass
            # Execute the operation for 10101111
        elif instruction == [1, 0, 1, 1, 0, 0, 0, 0]:
            pass
            # Execute the operation for 10110000
        elif instruction == [1, 0, 1, 1, 0, 0, 0, 1]:
            self.ora('C')

        elif instruction == [1, 0, 1, 1, 0, 0, 1, 0]:
            pass
            # Execute the operation for 10110010
        elif instruction == [1, 0, 1, 1, 0, 0, 1, 1]:
            pass
            # Execute the operation for 10110011
        elif instruction == [1, 0, 1, 1, 0, 1, 0, 0]:
            pass
            # Execute the operation for 10110100
        elif instruction == [1, 0, 1, 1, 0, 1, 0, 1]:
            pass
            # Execute the operation for 10110101
        elif instruction == [1, 0, 1, 1, 0, 1, 1, 0]:
            pass
            # Execute the operation for 10110110
        elif instruction == [1, 0, 1, 1, 0, 1, 1, 1]:
            pass
            # Execute the operation for 10110111
        elif instruction == [1, 0, 1, 1, 1, 0, 0, 0]:
            pass
            # Execute the operation for 10111000
        elif instruction == [1, 0, 1, 1, 1, 0, 0, 1]:
            pass
            # Execute the operation for 10111001
        elif instruction == [1, 0, 1, 1, 1, 0, 1, 0]:
            pass
            # Execute the operation for 10111010
        elif instruction == [1, 0, 1, 1, 1, 0, 1, 1]:
            pass
            # Execute the operation for 10111011
        elif instruction == [1, 0, 1, 1, 1, 1, 0, 0]:
            pass
            # Execute the operation for 10111100
        elif instruction == [1, 0, 1, 1, 1, 1, 0, 1]:
            pass
            # Execute the operation for 10111101
        elif instruction == [1, 0, 1, 1, 1, 1, 1, 0]:
            pass
            # Execute the operation for 10111110
        elif instruction == [1, 0, 1, 1, 1, 1, 1, 1]:
            pass
            # Execute the operation for 10111111
        elif instruction == [1, 1, 0, 0, 0, 0, 0, 0]:
            pass
            # Execute the operation for 11000000
        elif instruction == [1, 1, 0, 0, 0, 0, 0, 1]:
            pass
            # Execute the operation for 11000001
        elif instruction == [1, 1, 0, 0, 0, 0, 1, 0]:
            self.inx('PC')
            lb = self.mem.io(0, self.reg_r('PC'))
            self.inx('PC')
            hb = self.mem.io(0, self.reg_r('PC'))
            addr = lb + hb
            if not self.get_Z():
                self.jmp(addr)
            
        elif instruction == [1, 1, 0, 0, 0, 0, 1, 1]:
            pass
            # Execute the operation for 11000011
        elif instruction == [1, 1, 0, 0, 0, 1, 0, 0]:
            pass
            # Execute the operation for 11000100
        elif instruction == [1, 1, 0, 0, 0, 1, 0, 1]:
            pass
            # Execute the operation for 11000101
        elif instruction == [1, 1, 0, 0, 0, 1, 1, 0]:
            pass
            # Execute the operation for 11000110
        elif instruction == [1, 1, 0, 0, 0, 1, 1, 1]:
            pass
            # Execute the operation for 11000111
        elif instruction == [1, 1, 0, 0, 1, 0, 0, 0]:
            if self.get_Z():
                self.ret()

        elif instruction == [1, 1, 0, 0, 1, 0, 0, 1]:
            self.ret()

        elif instruction == [1, 1, 0, 0, 1, 0, 1, 0]:
            pass
            # Execute the operation for 11001010
        elif instruction == [1, 1, 0, 0, 1, 0, 1, 1]:
            pass
            # Execute the operation for 11001011
        elif instruction == [1, 1, 0, 0, 1, 1, 0, 0]:
            pass
            # Execute the operation for 11001100
        elif instruction == [1, 1, 0, 0, 1, 1, 0, 1]:
            pass
            # Execute the operation for 11001101
        elif instruction == [1, 1, 0, 0, 1, 1, 1, 0]:
            pass
            # Execute the operation for 11001110
        elif instruction == [1, 1, 0, 0, 1, 1, 1, 1]:
            pass
            # Execute the operation for 11001111
        elif instruction == [1, 1, 0, 1, 0, 0, 0, 0]:
            pass
            # Execute the operation for 11010000
        elif instruction == [1, 1, 0, 1, 0, 0, 0, 1]:
            pass
            # Execute the operation for 11010001
        elif instruction == [1, 1, 0, 1, 0, 0, 1, 0]:
            pass
            # Execute the operation for 11010010
        elif instruction == [1, 1, 0, 1, 0, 0, 1, 1]:
            pass
            # Execute the operation for 11010011
        elif instruction == [1, 1, 0, 1, 0, 1, 0, 0]:
            pass
            # Execute the operation for 11010100
        elif instruction == [1, 1, 0, 1, 0, 1, 0, 1]:
            pass
            # Execute the operation for 11010101
        elif instruction == [1, 1, 0, 1, 0, 1, 1, 0]:
            pass
            # Execute the operation for 11010110
        elif instruction == [1, 1, 0, 1, 0, 1, 1, 1]:
            pass
            # Execute the operation for 11010111
        elif instruction == [1, 1, 0, 1, 1, 0, 0, 0]:
            pass
            # Execute the operation for 11011000
        elif instruction == [1, 1, 0, 1, 1, 0, 0, 1]:
            pass
            # Execute the operation for 11011001
        elif instruction == [1, 1, 0, 1, 1, 0, 1, 0]:
            pass
            # Execute the operation for 11011010
        elif instruction == [1, 1, 0, 1, 1, 0, 1, 1]:
            pass
            # Execute the operation for 11011011
        elif instruction == [1, 1, 0, 1, 1, 1, 0, 0]:
            pass
            # Execute the operation for 11011100
        elif instruction == [1, 1, 0, 1, 1, 1, 0, 1]:
            pass
            # Execute the operation for 11011101
        elif instruction == [1, 1, 0, 1, 1, 1, 1, 0]:
            pass
            # Execute the operation for 11011110
        elif instruction == [1, 1, 0, 1, 1, 1, 1, 1]:
            pass
            # Execute the operation for 11011111
        elif instruction == [1, 1, 1, 0, 0, 0, 0, 0]:
            pass
            # Execute the operation for 11100000
        elif instruction == [1, 1, 1, 0, 0, 0, 0, 1]:
            pass
            # Execute the operation for 11100001
        elif instruction == [1, 1, 1, 0, 0, 0, 1, 0]:
            pass
            # Execute the operation for 11100010
        elif instruction == [1, 1, 1, 0, 0, 0, 1, 1]:
            pass
            # Execute the operation for 11100011
        elif instruction == [1, 1, 1, 0, 0, 1, 0, 0]:
            pass
            # Execute the operation for 11100100
        elif instruction == [1, 1, 1, 0, 0, 1, 0, 1]:
            pass
            # Execute the operation for 11100101
        elif instruction == [1, 1, 1, 0, 0, 1, 1, 0]:
            pass
            # Execute the operation for 11100110
        elif instruction == [1, 1, 1, 0, 0, 1, 1, 1]:
            pass
            # Execute the operation for 11100111
        elif instruction == [1, 1, 1, 0, 1, 0, 0, 0]:
            pass
            # Execute the operation for 11101000
        elif instruction == [1, 1, 1, 0, 1, 0, 0, 1]:
            pass
            # Execute the operation for 11101001
        elif instruction == [1, 1, 1, 0, 1, 0, 1, 0]:
            pass
            # Execute the operation for 11101010
        elif instruction == [1, 1, 1, 0, 1, 0, 1, 1]:
            pass
            # Execute the operation for 11101011
        elif instruction == [1, 1, 1, 0, 1, 1, 0, 0]:
            pass
            # Execute the operation for 11101100
        elif instruction == [1, 1, 1, 0, 1, 1, 0, 1]:
            pass
            # Execute the operation for 11101101
        elif instruction == [1, 1, 1, 0, 1, 1, 1, 0]:
            pass
            # Execute the operation for 11101110
        elif instruction == [1, 1, 1, 0, 1, 1, 1, 1]:
            pass
            # Execute the operation for 11101111
        elif instruction == [1, 1, 1, 1, 0, 0, 0, 0]:
            pass
            # Execute the operation for 11110000
        elif instruction == [1, 1, 1, 1, 0, 0, 0, 1]:
            pass
            # Execute the operation for 11110001
        elif instruction == [1, 1, 1, 1, 0, 0, 1, 0]:
            pass
            # Execute the operation for 11110010
        elif instruction == [1, 1, 1, 1, 0, 0, 1, 1]:
            pass
            # Execute the operation for 11110011
        elif instruction == [1, 1, 1, 1, 0, 1, 0, 0]:
            pass
            # Execute the operation for 11110100
        elif instruction == [1, 1, 1, 1, 0, 1, 0, 1]:
            pass
            # Execute the operation for 11110101
        elif instruction == [1, 1, 1, 1, 0, 1, 1, 0]:
            pass
            # Execute the operation for 11110110
        elif instruction == [1, 1, 1, 1, 0, 1, 1, 1]:
            pass
            # Execute the operation for 11110111
        elif instruction == [1, 1, 1, 1, 1, 0, 0, 0]:
            pass
            # Execute the operation for 11111000
        elif instruction == [1, 1, 1, 1, 1, 0, 0, 1]:
            pass
            # Execute the operation for 11111001
        elif instruction == [1, 1, 1, 1, 1, 0, 1, 0]:
            pass
            # Execute the operation for 11111010
        elif instruction == [1, 1, 1, 1, 1, 0, 1, 1]:
            pass
            # Execute the operation for 11111011
        elif instruction == [1, 1, 1, 1, 1, 1, 0, 0]:
            pass
            # Execute the operation for 11111100
        elif instruction == [1, 1, 1, 1, 1, 1, 0, 1]:
            pass
            # Execute the operation for 11111101
        elif instruction == [1, 1, 1, 1, 1, 1, 1, 0]:
            pass
            # Execute the operation for 11111110
        elif instruction == [1, 1, 1, 1, 1, 1, 1, 1]:
            pass
            # Execute the operation for 11111111
        else:
            return EXIT_ERROR
        self.inx('PC')

    def run(self):
        while True:
            instruction = self.fetch()
            if instruction == [0,0,0,0,0,0,0,0]:
                break
            else:
                self.execute(instruction)
                if self.bits_to_int(self.reg_r('PC')) >= 65535:  # 假设停止条件
                    break
            