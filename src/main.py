import numpy as np
from scipy.ndimage.measurements import label


def main(input):
    grid = np.array(input["rows"])

    buildings = []

    heights = sorted(np.unique(grid))
    for height in heights[1:]:
        grid_on_height = np.where(grid == height, grid, 0)

        mask, ncomponents = label(grid_on_height)

        # is the floor in the upper left corner?
        assert grid_on_height[0, 0] == 0

        for ncomponent in range(1, ncomponents + 1):
            building = get_building(grid_on_height, mask, ncomponent)
            hotspots = get_hotspots(grid_on_height, mask, building, ncomponent, input["s"])
            buildings.extend(hotspots)

    # sort by row and by col
    buildings = sorted(buildings, key=lambda x: (x[0], x[1]))

    # prepend id and only output upper left corner
    buildings = [(i, *a) for i, a in enumerate(buildings)]

    print(buildings)
    # [' '.join([' '.join(f) for f in e]) for e in buildings]
    result = ' '.join([' '.join(map(str, e)) for e in buildings])
    return result


def get_hotspots(grid, mask, building, ncomponent, size):
    r1, c1, r2, c2 = building
    hotspots_grid = np.zeros_like(mask)

    def _does_fit(row_, col_):
        # extract possible hotspot
        submatrix = mask[row_:row_ + size, col_:col_ + size]
        if submatrix.shape[0] != 3 or submatrix.shape[1] != 3:
            return False
        # check if all cells are on the building
        return np.all(submatrix == ncomponent)

    for row in range(r1, r2 + 1):
        for col in range(c1, c2 + 1):
            if _does_fit(row, col):
                hotspots_grid[row:row + size, col:col + size] = 1  # np.ones((size, size))

    # plt.imshow(hotspots_grid)
    # plt.show()

    hotspots_mask, nhotspots = label(hotspots_grid)

    # use the building algorithm again ...
    hotspots = []
    for nhotspots in range(1, nhotspots + 1):
        hotspot = get_building(hotspots_grid, hotspots_mask, nhotspots)
        hotspots.append(hotspot)

    # get center points of hotspots
    hotspots = [get_center_point(*a) for a in hotspots]

    # hotspot center must be in on the building
    hotspots = [e for e in hotspots if hotspots_grid[e[0], e[1]] == 1]

    return hotspots


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


def is_hotspot(size, r1, c1, r2, c2):
    return (r2 - r1) + 1 >= size \
           and (c2 - c1) + 1 >= size


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
