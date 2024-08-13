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
    def __init__(self, bins):
        self.bins = bins
        self.size = 64 * 1024 # 64KB memory [0x0000 to 0xFFFF] 16 bit address
        self.cells = [Byte() for i in range(self.size)]
    
    def act(self):
        rw = self.bins.WR
        addr = self.bins.A
        dbin = self.bins.DBIN
        data = self.bins.D
        addr_dec = addr_converter(addr)
        if not rw and not dbin:
            self.cells[addr_dec].write(data)
        elif rw and dbin:
            self.bins.D = self.cells[addr_dec].read()
        else:
            print("SSS")
