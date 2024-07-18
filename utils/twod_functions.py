from shapely.geometry import Polygon, Point

def generate_rectangle(width, height):
    return Polygon([(0, 0), (width, 0), (width, height), (0, height)])

def generate_circle(radius):
    return Point(0, 0).buffer(radius)

def generate_triangle(base, height):
    return Polygon([(0, 0), (base, 0), (base / 2, height)])

def is_valid_shape(shape):
    if not shape.is_valid:
        shape = shape.buffer(0)
    return shape.is_valid

def can_place(shape, boundary, placed_shapes):
    if not is_valid_shape(shape) or not shape.within(boundary):
        return False
    for placed in placed_shapes:
        if not is_valid_shape(placed):
            continue
        if shape.intersects(placed):
            return False
    return True