def addr_converter(addr):
    addr_dec = 0
    for i in range(16):
        addr_dec += addr[15 - i] * 2 ** i
    return addr_dec

class Program:
    def __init__(self):
        self.data = [[0, 1, 1, 1, 1, 0, 0, 0],
                     [1, 0, 1, 1, 0, 0, 0, 1],
                     [1, 1, 0, 0, 1, 0, 0, 0],
                     [0, 0, 0, 1, 1, 0, 1, 0],
                     [0, 1, 1, 1, 0, 1, 1, 1],
                     [0, 0, 0, 1, 0, 0, 1, 1],
                     [0, 0, 1, 0, 0, 0, 1, 1],
                     [0, 0, 0, 0, 1, 0, 1, 1],
                     [0, 1, 1, 1, 1, 0, 0, 0],
                     [1, 0, 1, 1, 0, 0, 0, 1],
                     [1, 1, 0, 0, 0, 0, 1, 0],
                     [0, 0, 0, 0, 0, 0, 1, 1],
                     [1, 1, 1, 0, 1, 0, 1, 1],
                     [1, 1, 0, 0, 1, 0, 0, 1],
                     [0, 0, 0, 0, 0, 0, 0, 0]]

    def load(self, addr):
        addr_dec = addr_converter(addr)
        return self.data[addr_dec]
