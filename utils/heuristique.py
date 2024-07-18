from utils.twod_functions import *

from shapely.affinity import rotate, translate

import numpy as np

def heuristique(boundary, shapes):
    placed_shapes = []
    
    for shape_data in shapes:
        
        best_position = None
        min_unused_space = float('inf')
        
        for x in np.arange(boundary.bounds[0], boundary.bounds[2], 0.2):
            for y in np.arange(boundary.bounds[1], boundary.bounds[3], 0.2):
                for angle in range(0, 360, 90):
                    rotated_shape = rotate(shape_data, angle, origin='centroid')
                    translated_shape = translate(rotated_shape, xoff=x, yoff=y)
                    if can_place(translated_shape, boundary, placed_shapes):
                        unused_space = boundary.area - sum([s.area for s in placed_shapes]) - translated_shape.area
                        if unused_space < min_unused_space:
                            min_unused_space = unused_space
                            best_position = translated_shape
        
        if best_position:
            placed_shapes.append(best_position)
    
    return placed_shapes