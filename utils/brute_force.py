from utils.twod_functions import *

from shapely.affinity import rotate, translate

import numpy as np

def brute_force(boundary, shapes):
    placed_shapes = []
    for shape_data in shapes:        
        placed = False
        for x in np.arange(boundary.bounds[0], boundary.bounds[2], 0.1):
            for y in np.arange(boundary.bounds[1], boundary.bounds[3], 0.1):
                for angle in range(0, 360, 90):
                    rotated_shape = rotate(shape_data, angle, origin=(0, 0))
                    translated_shape = translate(rotated_shape, xoff=x, yoff=y)
                    if can_place(translated_shape, boundary, placed_shapes):
                        placed_shapes.append(translated_shape)
                        placed = True
                        break
                if placed:
                    break
            if placed:
                break
    return placed_shapes