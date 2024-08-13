BITS_WIDE = 32
from memory import Memory

class CPU:
    def __init__(self, memory) -> None:
        self.reg = {
            '00000': [0] * BITS_WIDE, '00001': [0] * BITS_WIDE, '00010': [0] * BITS_WIDE, '00011': [0] * BITS_WIDE,
            '00100': [0] * BITS_WIDE, '00101': [0] * BITS_WIDE, '00110': [0] * BITS_WIDE, '00111': [0] * BITS_WIDE,
            '01000': [0] * BITS_WIDE, '01001': [0] * BITS_WIDE, '01010': [0] * BITS_WIDE, '01011': [0] * BITS_WIDE,
            '01100': [0] * BITS_WIDE, '01101': [0] * BITS_WIDE, '01110': [0] * BITS_WIDE, '01111': [0] * BITS_WIDE,
            '10000': [0] * BITS_WIDE, '10001': [0] * BITS_WIDE, '10010': [0] * BITS_WIDE, '10011': [0] * BITS_WIDE,
            '10100': [0] * BITS_WIDE, '10101': [0] * BITS_WIDE, '10110': [0] * BITS_WIDE, '10111': [0] * BITS_WIDE,
            '11000': [0] * BITS_WIDE, '11001': [0] * BITS_WIDE, '11010': [0] * BITS_WIDE, '11011': [0] * BITS_WIDE,
            '11100': [0] * BITS_WIDE, '11101': [0] * BITS_WIDE, '11110': [0] * BITS_WIDE, '11111': [0] * BITS_WIDE
        }
        self.memory = Memory()
        self.pc = [0] * BITS_WIDE
        self.hi = [0] * BITS_WIDE
        self.lo = [0] * BITS_WIDE

    def IF(self):
        instruction = self.memory.io(self.pc, 4)
        self.ID(instruction)
        self.pc += 4

    def ID(self, instruction):
        opcode = instruction[0:6]
        rs = instruction[6:11]
        rt = instruction[11:16]
        rd = instruction[16:21]
        funct = instruction[26:32]
        immediate = instruction[16:32]
        address = instruction[6:32]
        self.EXE(opcode, rs, rt, rd, funct, immediate, address)

    def EXE(self, opcode, rs, rt, rd, funct, immediate, address):
        if opcode == '000000':  # R-type instructions
            if funct == '100000':  # add
                self.add(rs, rt, rd)
            elif funct == '100010':  # sub
                self.sub(rs, rt, rd)
            elif funct == '011000':  # mult
                self.mult(rs, rt)
            elif funct == '011001':  # multu
                self.multu(rs, rt)
            elif funct == '011010':  # div
                self.div(rs, rt)
            elif funct == '011011':  # divu
                self.divu(rs, rt)
            elif funct == '010000':  # mfhi
                self.mfhi(rd)
            elif funct == '010010':  # mflo
                self.mflo(rd)
            elif funct == '001000':  # jr
                self.jr(rs)
            elif funct == '001001':  # jalr
                self.jalr(rs)
            elif funct == '001100':  # lis
                self.lis(rd)
            elif funct == '101010':  # slt
                self.slt(rs, rt, rd)
            elif funct == '101011':  # sltu
                self.sltu(rs, rt, rd)
        elif opcode == '100011':  # lw
            self.lw(rs, rt, immediate)
        elif opcode == '101011':  # sw
            self.sw(rs, rt, immediate)
        elif opcode == '000100':  # beq
            self.beq(rs, rt, immediate)
        elif opcode == '000101':  # bne
            self.bne(rs, rt, immediate)
        elif opcode == '001000':  # addi
            self.addi(rs, rt, immediate)
        elif opcode == '000010':  # j
            self.j(address)
        elif opcode == '000011':  # jal
            self.jal(address)

    def MEM(self, resister, address, size, type=0):
        if type:
            self.memory.io(address, size, 1, self.reg[resister])
        else:
            self.WB(resister, self.memory.io(address, size))


    def WB(self, rd, data):
        self.reg[rd] = data

    def _word(self):
        pass

    def add(self, rs, rt, rd):
        pass

    def sub(self, rs, rt, rd):
        pass

    def mult(self, rs, rt):
        pass

    def multu(self, rs, rt):
        pass

    def div(self, rs, rt):
        pass

    def divu(self, rs, rt):
        pass

    def mfhi(self, rd):
        pass

    def mflo(self, rd):
        pass

    def lis(self, rd):
        pass

    def lw(self, rs, rt, i):
        pass

    def sw(self, rs, rt, i):
        pass

    def slt(self, rs, rt, rd):
        pass

    def sltu(self, rs, rt, rd):
        pass

    def beq(self, rs, rt, i):
        pass

    def bne(self, rs, rt, i):
        pass

    def jr(self, rs):
        pass

    def jalr(self, rs):
        pass

    def addi(self, rs, rt, i):
        pass

    def j(self, i):
        pass

    def jal(self, i):
        pass
