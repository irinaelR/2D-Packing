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
    
    def get_remaining_surface(self):
        return self.size - self.get_occupied_surface()

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

def best_fit(shapes, B):
    bacs = [Bac([], B)] # we begin with one empty bac of the size B

    for shape in shapes:

        if shape.size <= B:

            min_space_left = float('inf')
            bac_index = -1

            for index, bac in enumerate(bacs):

                space_left = bac.get_remaining_surface() - shape.size

                if min_space_left > space_left and space_left >= 0:
                    # minimizing the space left after insertion AND making sure the shape can actually fit
                    bac_index = index
                    min_space_left = space_left
            
            if bac_index >= 0:
                # a valid bac was found to insert the shape into
                bacs[bac_index].shapes.append(shape)
            else:
                # we add a new bac to accomodate
                bacs.append(Bac([shape], B))

    return bacs
            
def worst_fit(shapes, B):
    bacs = [Bac([], B)] # we begin with one empty bac of the size B

    for shape in shapes:

        if shape.size <= B:

            max_space_left = -float('inf') - 1
            bac_index = -1

            for index, bac in enumerate(bacs):

                space_left = bac.get_remaining_surface() - shape.size

                if max_space_left < space_left and space_left >= 0:
                    # minimizing the space left after insertion AND making sure the shape can actually fit
                    bac_index = index
                    max_space_left = space_left
            
            if bac_index >= 0:
                # a valid bac was found to insert the shape into
                bacs[bac_index].shapes.append(shape)
            else:
                # we add a new bac to accomodate
                bacs.append(Bac([shape], B))

    return bacs

import itertools
def brute_force(shapes, B):
    best_layout = None
    min_nb = float('inf')

    # permutation of the order of insertion of the shapes
    for permutation in itertools.permutations(shapes):
        bacs = []
        for shape in permutation:
            added = False
            for b in bacs:
                if b.get_occupied_surface() + shape.size <= b.size:
                    b.shapes.append(shape)
                    added = True
                    break

            if not added:
                bacs.append(Bac([shape], B))
        
        if len(bacs) <= min_nb:
            min_nb = len(bacs)
            best_layout = bacs

    return best_layout

B = 10
shapes = [Shape(5), Shape(2), Shape(4), Shape(1), Shape(3), Shape(4)]

print("First Fit 1D")
filled_bacs = first_fit(shapes, B)
    # i want to print the bac's index and its shapes array (bac.shapes)
for index, bac in enumerate(filled_bacs):
    print(f"Bac index: {index}, Shapes: {[shape.size for shape in bac.shapes]}")

print("Best Fit 1D")
filled_bacs = best_fit(shapes, B)
    # i want to print the bac's index and its shapes array (bac.shapes)
for index, bac in enumerate(filled_bacs):
    print(f"Bac index: {index}, Shapes: {[shape.size for shape in bac.shapes]}")

print("worst Fit 1D")
filled_bacs = worst_fit(shapes, B)
    # i want to print the bac's index and its shapes array (bac.shapes)
for index, bac in enumerate(filled_bacs):
    print(f"Bac index: {index}, Shapes: {[shape.size for shape in bac.shapes]}")

print("Brute force 1D")
filled_bacs = brute_force(shapes, B)
    # i want to print the bac's index and its shapes array (bac.shapes)
for index, bac in enumerate(filled_bacs):
    print(f"Bac index: {index}, Shapes: {[shape.size for shape in bac.shapes]}")
