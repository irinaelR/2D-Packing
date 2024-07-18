'''"Mandeha"''' 
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point
from shapely.affinity import rotate, translate
import numpy as np

boundary = Polygon([(0, 0), (10, 0), (10, 10), (0, 10)])

shapes = [
    {'type': 'rectangle', 'width': 1, 'height': 2},
    {'type': 'circle', 'radius': 1},
    {'type': 'triangle', 'base': 3, 'height': 2},
    {'type': 'rectangle', 'width': 2, 'height': 1},
    {'type': 'circle', 'radius': 0.5},
    {'type': 'triangle', 'base': 2, 'height': 1.5},
    {'type': 'triangle', 'base': 2, 'height': 1.5},
    {'type': 'triangle', 'base': 2, 'height': 1.5},
    {'type': 'triangle', 'base': 2, 'height': 1.5},
    {'type': 'triangle', 'base': 2, 'height': 1.5},
    {'type': 'triangle', 'base': 2, 'height': 1.5},
]

def generate_rectangle(width, height):
    return Polygon([(0, 0), (width, 0), (width, height), (0, height)])

def generate_circle(radius):
    return Point(0, 0).buffer(radius)

def generate_triangle(base, height):
    return Polygon([(0, 0), (base, 0), (base / 2, height)])

def can_place(shape, boundary, placed_shapes):
    if not shape.within(boundary):
        return False
    for placed in placed_shapes:
        if shape.intersects(placed):
            return False
    return True

def pack_shapes(boundary, shapes):
    placed_shapes = []
    for shape_data in shapes:
        shape_type = shape_data['type']
        if shape_type == 'rectangle':
            shape = generate_rectangle(shape_data['width'], shape_data['height'])
        elif shape_type == 'circle':
            shape = generate_circle(shape_data['radius'])
        elif shape_type == 'triangle':
            shape = generate_triangle(shape_data['base'], shape_data['height'])
        
        placed = False
        for x in np.arange(boundary.bounds[0], boundary.bounds[2], 0.1):
            for y in np.arange(boundary.bounds[1], boundary.bounds[3], 0.1):
                for angle in range(0, 360, 90):
                    rotated_shape = rotate(shape, angle, origin=(0, 0))
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

placed_shapes = pack_shapes(boundary, shapes)

fig, ax = plt.subplots()
for shape in placed_shapes:
    x, y = shape.exterior.xy
    ax.plot(x, y)
x, y = boundary.exterior.xy
ax.plot(x, y)

plt.show()