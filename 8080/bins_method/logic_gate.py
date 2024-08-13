def neg(a):
    if a == 0:
        return 1
    else:
        return 0


def land(a, b):
    return a * b


def lor(a, b):
    if (a + b) == 0:
        return 0
    else:
        return 1


def lnand(a, b):
    return neg(land(a, b))


def lnor(a, b):
    return neg(lor(a, b))


