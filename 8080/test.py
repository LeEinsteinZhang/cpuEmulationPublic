from cpu import *
from memory import *

c1 = CPU(Memory()) # initial
c1.mem.cells[32].write([1, 0, 1, 1, 0, 0, 1, 1])              # set 32 cells
address = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]    # pre define a address use 16-bit list
address_31 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1] # pre define a address use 16-bit list
c1.reg_w('A', [0, 0, 0, 0, 0, 0, 0, 1])                        # set reg A value

#mov lda test
c1.mov('B', 'A')
print("mov test pass?=",(c1.reg_r('B') == [0, 0, 0, 0, 0, 0, 0, 1]))
c1.lda(address)

print("lda test pass?=",c1.reg_r('A') == [1, 0, 1, 1, 0, 0, 1, 1])

#sta test
c1.reg_w('A', [1, 0, 0, 0, 0, 0, 0, 0])
c1.sta(address_31)
print("sta test pass?=",c1.mem.cells[31].read() == [1, 0, 0, 0, 0, 0, 0, 0])

#add test
c1.reg_w('A', c1.int_to_bits_8b(1))
c1.reg_w('B', c1.int_to_bits_8b(1))
c1.add('B')
print("add test pass?=",c1.reg_r('A') == c1.int_to_bits_8b(2))

#adi test
c1.adi(c1.int_to_bits_8b(16))
print("adi test pass?=",c1.reg_r('A') == c1.int_to_bits_8b(18))

#lhld shld
address_128 = c1.int_to_bits_16b(128)
address_129 = c1.int_to_bits_16b(129)

address_256 = c1.int_to_bits_16b(256)
address_257 = c1.int_to_bits_16b(257)

val_255 = c1.int_to_bits_8b(255)

c1.mem.io(1, address_128, [0, 0, 0, 0, 0, 0, 0, 1])
c1.mem.io(1, address_129, val_255)

c1.lhld(address_128)
print("lhld test pass?=",c1.reg_r('HL') == c1.int_to_bits_16b(511))
c1.shld(address_256)
print("shld test pass?=",(c1.mem.cells[256].read() == c1.mem.cells[128].read()) and (c1.mem.cells[257].read() == c1.mem.cells[129].read()))

#ldax test
c1.reg_w('BC', address_256)
c1.ldax('BC')
print("ldax test pass?=",c1.reg_r('A') == c1.mem.cells[256].read())

#sdax test
address_512 = c1.int_to_bits_16b(512)
c1.reg_w('DE', address_512)
c1.stax('DE')
print("sdax test pass?=",c1.reg_r('A') == c1.mem.cells[512].read())

#xchg test
old_de = c1.reg_r('DE')
old_hl = c1.reg_r('HL')
c1.xchg()
print("xchg test pass?=",(c1.reg_r('DE') == old_hl) and (c1.reg_r('HL') == old_de))

# def adc(self, S):
    

# def aci(self, I):
    

#sub test
c1.reg_w('A', c1.int_to_bits_8b(2))
c1.reg_w('B', c1.int_to_bits_8b(1))
c1.sub('B')
print("sub test pass?=",c1.reg_r('A') == c1.int_to_bits_8b(1))

#sui test
c1.reg_w('A', c1.int_to_bits_8b(129))
c1.sui(1)
print("sui test pass?=",c1.reg_r('A') == c1.int_to_bits_8b(128))

# def sbb(self, S):
    

# def sbi(self, I):
    

# def inr(self, D):
    

# def dcr(self, D):
    

# def inx(self, RP):
    

# def dcx(self, RP):
    

# def dad(self, RP):
    

# def daa(self):
    

# def ana(self, S):
    

# def ani(self, I):
    

#ora test
c1.reg_w('A', [1,0,1,0,1,0,1,0])
c1.reg_w('B', [0,1,0,1,0,1,0,1])
c1.ora('B')
print("ora test pass?=",c1.reg_r('A') == [1,1,1,1,1,1,1,1])

# def adc(self, S):
#     pass

# def aci(self, I):
#     pass

# def sub(self, S):
#     pass

# def sui(self, I):
#     pass

# def sbb(self, S):
#     pass

# def sbi(self, I):
#     pass

# def inr(self, D):
#     pass

# def dcr(self, D):
#     pass

#inx test
c1.reg_w('DE', c1.int_to_bits_16b(1))
c1.inx('DE')
print("inx test pass?=",c1.reg_r('DE') == c1.int_to_bits_16b(2))

#dcx test
c1.dcx('DE')
print("dcx test pass?=",c1.reg_r('DE') == c1.int_to_bits_16b(1))

#push test
c1.reg_w('BC', c1.int_to_bits_16b(128))
c1.reg_w('SP',c1.int_to_bits_16b(65535))
c1.push('BC')
print("push test pass?=", c1.mem.cells[65533].read() + c1.mem.cells[65534].read() == c1.int_to_bits_16b(128))

#pop test
c1.pop('DE')
print("pop test pass?=",c1.reg_r('DE') == c1.int_to_bits_16b(128))

#xthl test
c1.push('DE')
old_sp_data = c1.mem.cells[65533].read() + c1.mem.cells[65534].read()
old_hl = c1.reg_r('HL')
c1.xthl()
print("xthl test pass?=",(c1.mem.cells[65533].read() + c1.mem.cells[65534].read() == old_hl) and (c1.reg_r('HL') == old_sp_data))



# asm code encoding tests
c2 = CPU(Memory()) # initial
n_bytes = 512
source_addr = 1024
target_addr = 2048
for i in range(n_bytes):
    c2.mem.cells[source_addr + i].write(c2.int_to_bits_8b(i))

#  memcpy --
#  Copy a block of memory from one location to another.
# 
#  Entry registers
#        BC - Number of bytes to copy
#        DE - Address of source data block
#        HL - Address of target data block
# 
#  Return registers
#        BC - Zero
c2.reg_w('BC', c2.int_to_bits_16b(n_bytes))
c2.reg_w('DE', c2.int_to_bits_16b(source_addr))
c2.reg_w('HL', c2.int_to_bits_16b(target_addr))
c2.reg_w('PC',  c2.int_to_bits_16b(1000))
c2.mem.cells[1000].write([0, 1, 1, 1, 1, 0, 0, 0]) #       mov a,b  ;Copy register B to register A
c2.mem.cells[1001].write([1, 0, 1, 1, 0, 0, 0, 1]) #       ora c    ;Bitwise OR of A and C into register A
c2.mem.cells[1002].write([1, 1, 0, 0, 1, 0, 0, 0]) #       rz       ;Return if the zero-flag is set high.
c2.mem.cells[1003].write([0, 0, 0, 1, 1, 0, 1, 0]) # loop: ldax d   ;Load A from the address pointed by DE
c2.mem.cells[1004].write([0, 1, 1, 1, 0, 1, 1, 1]) #       mov m,a  ;Store A into the address pointed by HL
c2.mem.cells[1005].write([0, 0, 0, 1, 0, 0, 1, 1]) #       inx d    ;Increment DE
c2.mem.cells[1006].write([0, 0, 1, 0, 0, 0, 1, 1]) #       inx h    ;Increment HL
c2.mem.cells[1007].write([0, 0, 0, 0, 1, 0, 1, 1]) #       dcx b    ;Decrement BC (does not affect Flags)
c2.mem.cells[1008].write([0, 1, 1, 1, 1, 0, 0, 0]) #       mov a,b  ;Copy B to A  (so as to compare BC with zero)
c2.mem.cells[1009].write([1, 0, 1, 1, 0, 0, 0, 1]) #       ora c    ;A = A | C    (are both B and C zero?)
c2.mem.cells[1010].write([1, 1, 0, 0, 0, 0, 1, 0]) #       jnz loop ;Jump to 'loop:' if the zero-flag is not set.
c2.mem.cells[1011].write([0, 0, 0, 0, 0, 0, 1, 1]) # <-|
c2.mem.cells[1012].write([1, 1, 1, 0, 1, 0, 1, 1]) # <-|-- 1003 int bits
c2.mem.cells[1013].write([1, 1, 0, 0, 1, 0, 0, 1]) #       ret      ;Return
# c2.mem.cells[1014].write([0, 0, 0, 0, 0, 0, 0, 0]) #       nop
c2.run()

same = True
for i in range(n_bytes):
    same = same and (c2.mem.cells[source_addr + i].read() == c2.mem.cells[target_addr + i].read())
print("memcpy asm tst pass?=",same)
