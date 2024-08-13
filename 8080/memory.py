def addr_converter(addr):
    addr_dec = 0
    for i in range(16):
        addr_dec += addr[15 - i] * 2 ** i
    return addr_dec

class Byte:
    def __init__(self):
        self.data = [0, 0, 0, 0, 0, 0, 0, 0]

    def write(self, data):
        if len(data) == 8 and all(bit in [0, 1] for bit in data):
            self.data = data
            return 1
        else:
            return 0

    def read(self):
        return self.data

    # def __repr__(self):
    #     return str(self.data)


class Memory:
    def __init__(self):
        self.size = 64 * 1024 # 64KB memory [0x0000 to 0xFFFF] 16 bit address
        self.cells = [Byte() for i in range(self.size)]

    def io(self, rw, addr, data=[0,0,0,0,0,0,0,0]):
        addr_dec = addr_converter(addr)
        if rw == 1:
            self.cells[addr_dec].write(data)
        elif rw == 0:
            return self.cells[addr_dec].read()
        else:
            return -1
