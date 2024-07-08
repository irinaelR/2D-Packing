import math
from Forms import Cercle
from Forms import Rectangle
from Forms import TriangleIsocele

def best_fit_heuristic(shapes, W, H):
    free_spaces = [(0, 0, W, H)]

    for shape in shapes:
        best_space = None
        min_waste = float('inf')

        for space in free_spaces:
            sx, sy, sw, sh = space

            if isinstance(shape, Cercle):
                if 2 * shape.rayon <= sw and 2 * shape.rayon <= sh:
                    waste = (sw - 2 * shape.rayon) * (sh - 2 * shape.rayon)
                    if waste < min_waste:
                        min_waste = waste
                        best_space = space

            elif isinstance(shape, Rectangle):
                original_width = shape.width
                original_height = shape.height
                for rot in [0, 90]:
                    if rot == 90:
                        shape.width, shape.height = original_height, original_width
                    if shape.width <= sw and shape.height <= sh:
                        waste = (sw - shape.width) * (sh - shape.height)
                        if waste < min_waste:
                            min_waste = waste
                            best_space = space
                shape.width, shape.height = original_width, original_height

            elif isinstance(shape, TriangleIsocele):
                original_base = shape.base
                original_height = shape.height
                for rot in [0, 90]:
                    if rot == 90:
                        shape.base, shape.height = original_height, original_base
                    if shape.base <= sw and shape.height <= sh:
                        waste = (sw - shape.base) * (sh - shape.height)
                        if waste < min_waste:
                            min_waste = waste
                            best_space = space
                shape.base, shape.height = original_base, original_height

        if best_space:
            sx, sy, sw, sh = best_space
            shape.x, shape.y = sx, sy

            if isinstance(shape, Cercle):
                used_width = 2 * shape.rayon
                used_height = 2 * shape.rayon
            elif isinstance(shape, Rectangle):
                used_width = shape.width
                used_height = shape.height
            elif isinstance(shape, TriangleIsocele):
                used_width = shape.base
                used_height = shape.height

            free_spaces.remove(best_space)
            new_spaces = [
                (sx + used_width, sy, sw - used_width, used_height),
                (sx, sy + used_height, sw, sh - used_height)
            ]
            valid_new_spaces = []
            for new_space in new_spaces:
                nsx, nsy, nsw, nsh = new_space
                if nsw > 0 and nsh > 0:
                    valid_new_spaces.append(new_space)
            free_spaces.extend(valid_new_spaces)

    return shapes

shapes = [
    Rectangle(6, 1), 
    Rectangle(1, 6), 
    Cercle(1), 
    TriangleIsocele(2, 1)
]
W, H = 8, 8
placed_shapes = best_fit_heuristic(shapes, W, H)

for shape in placed_shapes:
    if shape.x is not None and shape.y is not None:
        if isinstance(shape, Cercle):
            print(f'Cercle at ({shape.x}, {shape.y}) with radius {shape.rayon}')
        elif isinstance(shape, Rectangle):
            print(f'Rectangle at ({shape.x}, {shape.y}) with width {shape.width} and height {shape.height}')
        elif isinstance(shape, TriangleIsocele):
            print(f'Triangle at ({shape.x}, {shape.y}) with base {shape.base} and height {shape.height}')
    else:
        print(f'Shape could not be placed')