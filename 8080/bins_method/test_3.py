from bins import *
from bios import *
from cpu import *
from memory import *
from program import *

b1 = BINS()
m1 = Memory(b1)
p1 = Program(b1, "./add")
c1 = CPU(b1, m1, p1)

BIOS(c1)

print(c1.bits_to_int(m1.cells[4097].read() + m1.cells[4096].read()) == 579)
