from assembler import *

def load_binary_file(filename):
    """
    Load a binary text file and convert its content to a list of lists of integers.
    Each 8 bits (binary digits) in the file will be converted to a list of integers.

    :param filename: Path to the binary text file.
    :return: A list of lists of integers.
    """
    list_of_lists = []

    with open(filename, 'r') as file:
        # Read the entire content of the file
        binary_content = file.read()

        # Temporary list to store each byte
        byte = []

        # Iterate over each character in the binary content
        for i, char in enumerate(binary_content):
            bit = int(char)
            byte.append(bit)

            # Every 8 bits, append the byte to the list of lists and reset the byte list
            if (i + 1) % 8 == 0:
                list_of_lists.append(byte)
                byte = []

        # If there are remaining bits that don't make up a full byte, pad them with 0's
        if byte:
            byte += [0] * (8 - len(byte))
            list_of_lists.append(byte)

    return list_of_lists

class Program:
    def __init__(self, bins, filename):
        self.bins = bins
        self.program = load_binary_file(asm_bin(filename))
        self.i = 0

    def load(self):
        self.bins.D = self.program[self.i]
        self.i += 1

