def hex_to_decimal(hex_number):
    decimal_number = 0
    hex_digits = '0123456789ABCDEF'
    for power, digit in enumerate(hex_number[2:].upper()[::-1]):
        decimal_number += hex_digits.index(digit) * (16 ** power)
    return decimal_number

def decimal_to_binary(decimal_number, length=8):
    binary_list = []
    while decimal_number > 0:
        binary_list.insert(0, decimal_number % 2)
        decimal_number = decimal_number // 2
    while len(binary_list) < length:
        binary_list.insert(0, 0)

    return binary_list

def convert_to_twos_complement(binary_list):
    inverted = [1 if bit == 0 else 0 for bit in binary_list]
    carry = 1
    for i in range(len(inverted) - 1, -1, -1):
        if inverted[i] == 1 and carry == 1:
            inverted[i] = 0
            carry = 1
        elif carry == 1:
            inverted[i] += 1
            carry = 0
    return inverted

def convert_to_binary_list(number, length=8):
    is_negative = number.startswith('-')
    if number.lower().startswith('0x'):
        decimal_number = hex_to_decimal(number)
    else:
        decimal_number = int(number)
    if is_negative:
        decimal_number = abs(decimal_number)
    binary_list = decimal_to_binary(decimal_number, length)
    if is_negative:
        binary_list = convert_to_twos_complement(binary_list)
        binary_list[0] = 1

    return binary_list

print(hex_to_decimal("0xFFF"))