import numpy as np


def main(input):
    tuples = np.array(input["tuples"])

    result = ''
    for tuple in tuples:
        c = calculate(**tuple)
        result += c + '\n'

    return result


def calculate(r1, c1, r2, c2, ratio):
    a = np.array([r1 + 0.5, c1 + 0.5])
    b = np.array([r2 + 0.5, c2 + 0.5])
    t = b - a

    c = np.floor(ratio * t + a)

    return ' '.join(map(str, map(int, c)))
