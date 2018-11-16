import numpy as np


def main(input):
    tuples = np.array(input["tuples"])

    result = ''
    for tuple in tuples:
        c = paint_line(tuple, 0.001)
        result += c + '\n'

    return result


def paint_line(tuple, stepsize):
    cells = set()
    for ratio in np.arange(0, 1, stepsize):
        cell = intersection_cell(ratio, **tuple)
        cells.add(cell)

    return ' '.join(cells)


def intersection_cell(ratio, r1, c1, r2, c2):
    a = np.array([r1 + 0.5, c1 + 0.5])
    b = np.array([r2 + 0.5, c2 + 0.5])
    t = b - a

    c = np.floor(ratio * t + a)

    return ' '.join(map(str, map(int, c)))
