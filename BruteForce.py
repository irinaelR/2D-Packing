import itertools
import matplotlib.pyplot as plt
import matplotlib.patches as patches

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
            TriangleIsocele(shape.base, shape.height)
        ]

def brute_force_packing(shapes, W, H):
    best_placement = None
    min_bins = float('inf')

    rotations = [generate_rotations(shape) for shape in shapes]
    all_rotations_combinations = itertools.product(*rotations)
    
    for rotation_comb in all_rotations_combinations:
        placements = []

        def place_shape(i, current_placements, free_spaces):
            nonlocal best_placement, min_bins
            if i == len(rotation_comb):
                if len(current_placements) < min_bins:
                    min_bins = len(current_placements)
                    best_placement = list(current_placements)
                return
            
            shape = rotation_comb[i]
            placed = False
            for space in free_spaces:
                sx, sy, sw, sh = space
                if best_space_for_shape(shape, space):
                    shape.x, shape.y = sx, sy
                    current_placements.append(shape)
                    
                    new_free_spaces = []
                    for fsx, fsy, fsw, fsh in free_spaces:
                        if isinstance(shape, Cercle):
                            used_width = 2 * shape.rayon
                            used_height = 2 * shape.rayon
                        elif isinstance(shape, Rectangle):
                            used_width = shape.width
                            used_height = shape.height
                        elif isinstance(shape, TriangleIsocele):
                            if shape.rotation == 0 or shape.rotation == 180:
                                used_width = shape.base
                                used_height = shape.height
                            else:
                                used_width = shape.height
                                used_height = shape.base

                        new_spaces = [
                            (fsx + used_width, fsy, fsw - used_width, fsh),  # Droite
                            (fsx, fsy + used_height, fsw, fsh - used_height)  # Haut
                        ]
                        for nsx, nsy, nsw, nsh in new_spaces:
                            if nsw > 0 and nsh > 0:
                                new_free_spaces.append((nsx, nsy, nsw, nsh))
                    
                    place_shape(i + 1, current_placements, new_free_spaces)
                    
                    current_placements.pop()
                    placed = True
                    break
            
            if not placed:
                return
        
        free_spaces = [(0, 0, W, H)]
        place_shape(0, placements, free_spaces)
    
    return best_placement

def best_space_for_shape(shape, space):
    sx, sy, sw, sh = space

    if isinstance(shape, Cercle):
        if 2 * shape.rayon <= sw and 2 * shape.rayon <= sh:
            return True

    elif isinstance(shape, Rectangle):
        original_width = shape.width
        original_height = shape.height
        for rot in [0, 90]:
            if rot == 90:
                shape.width, shape.height = original_height, original_width
            if shape.width <= sw and shape.height <= sh:
                return True
        shape.width, shape.height = original_width, original_height

    elif isinstance(shape, TriangleIsocele):
        original_base = shape.base
        original_height = shape.height
        for rot in [0, 90, 180]:
            if rot == 90 or rot == 180:
                shape.base, shape.height = shape.height, shape.base
            if shape.base <= sw and shape.height <= sh:
                return True
        shape.base, shape.height = original_base, original_height
    
    return False

def plot_shapes(placed_shapes, W, H):
    fig, ax = plt.subplots()
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)

    for shape in placed_shapes:
        if isinstance(shape, Cercle):
            circle = patches.Circle((shape.x + shape.rayon, shape.y + shape.rayon), shape.rayon, edgecolor='black', facecolor='blue', alpha=0.5)
            ax.add_patch(circle)
        elif isinstance(shape, Rectangle):
            rect = patches.Rectangle((shape.x, shape.y), shape.width, shape.height, edgecolor='black', facecolor='green', alpha=0.5)
            ax.add_patch(rect)
        elif isinstance(shape, TriangleIsocele):
            triangle = patches.Polygon([(shape.x, shape.y), (shape.x + shape.base, shape.y), (shape.x + shape.base / 2, shape.y + shape.height)], edgecolor='black', facecolor='red', alpha=0.5)
            ax.add_patch(triangle)

    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

shapes = [
    Cercle(1),
    Rectangle(4, 2),
    TriangleIsocele(3, 2),
    Rectangle(3, 2) 
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

plot_shapes(placed_shapes, W, H)