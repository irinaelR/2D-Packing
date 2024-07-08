import math

class Forme:
    def __init__(self):
        self.x = None
        self.y = None
        self.rotation = 0

class Cercle(Forme):
    def __init__(self, rayon):
        super().__init__()
        self.rayon = rayon

class Rectangle(Forme):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height

class TriangleIsocele(Forme):
    def __init__(self, base, height):
        super().__init__()
        self.base = base
        self.height = height
