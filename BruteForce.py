import itertools
from Forms import Cercle, Rectangle, TriangleIsocele

def generate_rotations(shape):
    if isinstance(shape, Cercle):
        return [shape]
    elif isinstance(shape, Rectangle):
        return [
            Rectangle(shape.width, shape.height),
            Rectangle(shape.height, shape.width)
        ]
    elif isinstance(shape, TriangleIsocele):
        return [
            TriangleIsocele(shape.base, shape.height),
            TriangleIsocele(shape.height, shape.base),
            TriangleIsocele(shape.base, shape.height)  # Rotation de 180 degrés est la même que 0 degrés
        ]

def can_place(shape, x, y, W, H, placed_shapes):
    if isinstance(shape, Cercle):
        if x + 2 * shape.rayon > W or y + 2 * shape.rayon > H:
            return False
        for other in placed_shapes:
            if isinstance(other, Cercle):
                if ((x - other.x) ** 2 + (y - other.y) ** 2) ** 0.5 < shape.rayon + other.rayon:
                    return False
            elif isinstance(other, Rectangle):
                if not (x >= other.x + other.width or
                        x + 2 * shape.rayon <= other.x or
                        y >= other.y + other.height or
                        y + 2 * shape.rayon <= other.y):
                    return False
            elif isinstance(other, TriangleIsocele):
                if not (x >= other.x + other.base or
                        x + 2 * shape.rayon <= other.x or
                        y >= other.y + other.height or
                        y + 2 * shape.rayon <= other.y):
                    return False
        return True
    elif isinstance(shape, Rectangle):
        if x + shape.width > W or y + shape.height > H:
            return False
        for other in placed_shapes:
            if isinstance(other, Cercle):
                if not (x >= other.x + 2 * other.rayon or
                        x + shape.width <= other.x or
                        y >= other.y + 2 * other.rayon or
                        y + shape.height <= other.y):
                    return False
            elif isinstance(other, Rectangle):
                if not (x >= other.x + other.width or
                        x + shape.width <= other.x or
                        y >= other.y + other.height or
                        y + shape.height <= other.y):
                    return False
            elif isinstance(other, TriangleIsocele):
                if not (x >= other.x + other.base or
                        x + shape.width <= other.x or
                        y >= other.y + other.height or
                        y + shape.height <= other.y):
                    return False
        return True
    elif isinstance(shape, TriangleIsocele):
        if x + shape.base > W or y + shape.height > H:
            return False
        for other in placed_shapes:
            if isinstance(other, Cercle):
                if not (x >= other.x + 2 * other.rayon or
                        x + shape.base <= other.x or
                        y >= other.y + 2 * other.rayon or
                        y + shape.height <= other.y):
                    return False
            elif isinstance(other, Rectangle):
                if not (x >= other.x + other.width or
                        x + shape.base <= other.x or
                        y >= other.y + other.height or
                        y + shape.height <= other.y):
                    return False
            elif isinstance(other, TriangleIsocele):
                if not (x >= other.x + other.base or
                        x + shape.base <= other.x or
                        y >= other.y + other.height or
                        y + shape.height <= other.y):
                    return False
        return True

def brute_force_packing(shapes, W, H):
    best_placement = None
    min_bins = float('inf')

    rotations = [generate_rotations(shape) for shape in shapes]
    all_rotations_combinations = list(itertools.product(*rotations))
    
    for rotation_comb in all_rotations_combinations:
        placements = []

        def place_shape(i, current_placements):
            nonlocal best_placement, min_bins
            if i == len(rotation_comb):
                if len(current_placements) < min_bins:
                    min_bins = len(current_placements)
                    best_placement = list(current_placements)
                return
            
            shape = rotation_comb[i]
            for x in range(W):
                for y in range(H):
                    if can_place(shape, x, y, W, H, current_placements):
                        shape.x, shape.y = x, y
                        current_placements.append(shape)
                        place_shape(i + 1, current_placements)
                        current_placements.pop()
        
        place_shape(0, placements)
    
    return best_placement

shapes = [
    Rectangle(3, 2), 
    TriangleIsocele(3, 2),
    Cercle(1) 
]
W, H = 6, 6
placed_shapes = brute_force_packing(shapes, W, H)

for shape in placed_shapes:
    if isinstance(shape, Cercle):
        print(f'Cercle at ({shape.x}, {shape.y}) with radius {shape.rayon}')
    elif isinstance(shape, Rectangle):
        print(f'Rectangle at ({shape.x}, {shape.y}) with width {shape.width} and height {shape.height}')
    elif isinstance(shape, TriangleIsocele):
        print(f'Triangle at ({shape.x}, {shape.y}) with base {shape.base} and height {shape.height}')
