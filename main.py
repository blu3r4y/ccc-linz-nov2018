import numpy as np


def main(input):
    grid = np.array(input["rows"])
    heights = sorted(np.unique(grid))
    return ' '.join(map(str, heights[1:]))
