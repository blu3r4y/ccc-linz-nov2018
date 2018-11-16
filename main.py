import numpy as np
from scipy.ndimage.measurements import label


def main(input):
    grid = np.array(input["rows"])

    mask, ncomponents = label(grid)

    # is the floor in the upper left corner?
    assert grid[0, 0] == 0

    buildings = []
    for ncomponent in range(1, ncomponents + 1):
        building = get_building(grid, mask, ncomponent)

        is_hot = is_hotspot(*building)
        if is_hot:
            buildings.append(building)

    # get center points
    buildings = [get_center_point(*a) for a in buildings]

    # sort by row and by col
    buildings = sorted(buildings, key=lambda x: (x[0], x[1]))

    # prepend id and only output upper left corner
    buildings = [(i, *a) for i, a in enumerate(buildings)]

    print(buildings)
    # [' '.join([' '.join(f) for f in e]) for e in buildings]
    result = ' '.join([' '.join(map(str, e)) for e in buildings])
    return result


def get_building(grid, mask, building_index):
    r1, c1 = None, None
    r2, c2 = None, None
    for i, row in enumerate(mask):
        if any(row == building_index):
            fr = i
            fc_start = np.argmax(row == building_index)
            fc_end = len(row) - 1 - np.argmax(row[::-1] == building_index)

            # set upper left corner point (first match)
            if not r1 and not c1:
                r1, c1 = fr, fc_start

    # lower right corner point (last match)
    r2, c2 = fr, fc_end

    return r1, c1, r2, c2


def is_hotspot(r1, c1, r2, c2):
    min_row = 4
    min_col = 4
    return (r2 - r1) + 1 >= min_row \
           and (c2 - c1) + 1 >= min_col


def get_center_point(r1, c1, r2, c2):
    rx = r1 + (r2 - r1) // 2
    cx = c1 + (c2 - c1) // 2
    return rx, cx


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
