from cpu import *
def BIOS(cpu):
    cpu.mem.cells[0].write([0, 0, 1, 1, 0, 0, 0, 1])        # lxi sp,I
    cpu.mem.cells[1].write([1, 1, 1, 1, 1, 1, 1, 1])        # I_1
    cpu.mem.cells[2].write([1, 1, 1, 1, 1, 1, 1, 1])        # I_2
    
    # set program start location (16)
    cpu.mem.cells[3].write([0, 0, 1, 0, 0, 0, 0, 1])        # lxi m,I
    cpu.mem.cells[4].write([0, 0, 0, 0, 0, 0, 0, 0])        # I_1
    cpu.mem.cells[5].write([0, 0, 0, 1, 0, 0, 0, 0])        # I_2

    #
    cpu.mem.cells[6].write([1, 1, 0, 0, 1, 0, 0, 0])  #       rz
    cpu.mem.cells[7].write([1, 1, 0, 1, 1, 0, 1, 1])  # loop: in
    cpu.mem.cells[8].write([0, 0, 1, 0, 1, 0, 1, 0])  #       stax hl
    cpu.mem.cells[9].write([0, 0, 1, 0, 0, 0, 1, 1])  #       inx hl
    cpu.mem.cells[10].write([1, 1, 1, 1, 1, 1, 1, 0]) #       cpi 
    cpu.mem.cells[11].write([1, 1, 0, 0, 1, 0, 0, 1]) # <-| ret
    cpu.mem.cells[12].write([1, 1, 0, 0, 0, 0, 1, 0]) #       jnz loop
    cpu.mem.cells[13].write([0, 0, 0, 0, 0, 0, 0, 0]) # <-|
    cpu.mem.cells[14].write([0, 0, 0, 0, 0, 1, 1, 1]) # <-| 7

    cpu.run()
