from bins import *
from bios import *
from cpu import *
from memory import *
from program import *

b1 = BINS()
m1 = Memory(b1)
c1 = CPU(b1, m1, 0)

c1.mem.cells[0].write([0, 1, 1, 1, 1, 0, 0, 0])

c1.lda([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
print("lda test:", c1.reg_r('A') == [0, 1, 1, 1, 1, 0, 0, 0])
c1.mem.cells[0].write([0,0,0,0,0,0,0,0])
c1.sta([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
print("sta test:", c1.mem.cells[0].read() == [0, 1, 1, 1, 1, 0, 0, 0])


c1.lhld([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
print("lhld test:", c1.reg_r('HL') == [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0])

c1.shld([0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0])
print("shld test:", c1.mem.cells[4].read() == [0, 1, 1, 1, 1, 0, 0, 0])


# asm code encoding tests
b2 = BINS()
m2 = Memory(b2)
c2 = CPU(b2, m2, 0)
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


b3 = BINS()
m3 = Memory(b3)
p3 = Program(b3, "./memcpy")
c3 = CPU(b3, m3, p3)

n_bytes = 512
source_addr = 1024
target_addr = 2048
for i in range(n_bytes):
    c3.mem.cells[source_addr + i].write(c3.int_to_bits_8b(i))

BIOS(c3)

# after bios built in program loader following will load into memory

# The following program are shown in wikipedia:
# https://en.wikipedia.org/wiki/Intel_8080#

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

# 15 00000001 lxi bc         ; Load BC immediate  <= program start point 15
# 16 00000001 <-|
# 17 00000000 <-|-- 512

# 18 00010001       lxi de   ; Load DE immediate
# 29 00000100 <-|
# 20 00000000 <-|-- 1024

# 21 00100001       lxi hl   ; Load HL immediate
# 22 00001000 <-|
# 23 00000000 <-|-- 2048

# 24 01111000       mov a,b  ;Copy register B to register A

# 25 10110001       ora c    ;Bitwise OR of A and C into register A

# 26 11001000       rz       ;Return if the zero-flag is set high.

# 27 00011010 loop: ldax d   ;Load A from the address pointed by DE

# 28 01110111       mov m,a  ;Store A into the address pointed by HL

# 29 00010011       inx d    ;Increment DE

# 30 00100011       inx h    ;Increment HL

# 31 00001011       dcx b    ;Decrement BC (does not affect Flags)

# 32 01111000       mov a,b  ;Copy B to A  (so as to compare BC with zero)

# 33 10110001       ora c    ;A = A | C    (are both B and C zero?)

# 34 11000010       jnz loop ;Jump to 'loop:' if the zero-flag is not set
# 35 00000000 <-|
# 36 00011011 <-|-- 27

# 37 11001001       ret      ;Return

same = True
for i in range(n_bytes):
    # print(c3.mem.cells[source_addr + i].read(), c3.mem.cells[target_addr + i].read())
    same = same and (c3.mem.cells[source_addr + i].read() == c3.mem.cells[target_addr + i].read())
print("memcpy asm tst pass?=",same)
