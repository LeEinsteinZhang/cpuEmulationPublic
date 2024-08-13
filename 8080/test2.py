from cpu import *
from memory import *
from bios import *

# cpu init
c1 = CPU()
m1 = Memory()
BIOS(c1, m1)