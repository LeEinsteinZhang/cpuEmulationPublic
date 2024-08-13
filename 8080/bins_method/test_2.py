from bins import *
from bios import *
from cpu import *
from memory import *
from program import *

b1 = BINS()
m1 = Memory(b1)
p1 = Program(b1, "./memcpy")
c1 = CPU(b1, m1, p1)

BIOS(c1)

same = True
for i in range(512):
    # print(c3.mem.cells[source_addr + i].read(), c3.mem.cells[target_addr + i].read())
    same = same and (c1.mem.cells[1024 + i].read() == c1.mem.cells[2048 + i].read())
print("memcpy asm tst pass?=",same)