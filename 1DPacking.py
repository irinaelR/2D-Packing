class Shape:
    def __init__(self, size):
        self.size = size

class Bac(Shape):
    def __init__(self, shapes, B):
        # B is the fixed bac size
        super().__init__(B)
        self.shapes = shapes

    def get_occupied_surface(self):
        surface = 0

        for shape in self.shapes:
            surface += shape.size

        return surface

def first_fit(shapes, B):
    bacs = [Bac([], B)] # we begin with one empty bac of the size B

    for shape in shapes:
        if shape.size <= B:
            for bac in bacs:
                added = False
                occupied_surface = bac.get_occupied_surface()
                if occupied_surface + shape.size <= bac.size:
                    bac.shapes.append(shape)
                    added = True
                    break
            
            # if none of the bacs could fit the shape, we create a new one
            if not added:
                bacs.append(Bac([shape], B))

    return bacs

B = 2
shapes = [Shape(4), Shape(2), Shape(1), Shape(4), Shape(3)]

filled_bacs = first_fit(shapes, B)
    # i want to print the bac's index and its shapes array (bac.shapes)
for index, bac in enumerate(filled_bacs):
    print(f"Bac index: {index}, Shapes: {[shape.size for shape in bac.shapes]}")