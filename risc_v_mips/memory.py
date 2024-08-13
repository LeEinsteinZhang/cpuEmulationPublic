def addr_converter(addr):
    addr_dec = 0
    for i in range(32):
        addr_dec += int(addr[31 - i]) * 2 ** i
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

    def __repr__(self):
        return str(self.data)

class Memory:
    def __init__(self):
        self.size = 64 * 1024 # 64KB memory [0x00000000 to 0x0000FFFF] 32 bit address
        self.cells = [Byte() for _ in range(self.size)]

    def io(self, addr, size, type=0, data=[0,0,0,0,0,0,0]):
        addr_dec = addr_converter(addr)
        result = []
        if type == 1:
            for i in range(size):
                self.cells[addr_dec + i].write(data[i*8:(i+1)*8])
        elif type == 0:
            for i in range(size):
                result.extend(self.cells[addr_dec + i].read())
            return result
        else:
            return -1
