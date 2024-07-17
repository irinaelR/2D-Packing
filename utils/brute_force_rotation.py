import itertools
import copy

def brute_force_rotation(rectangles, W, H):
    for rectangle in rectangles:
        rectangle.x = None
        rectangle.y = None

    placed_rectangles = []

    for permutation in itertools.permutations(rectangles):
        temp_layout = []
        for rectangle in permutation:
            added = False
            rotated_rectangle = rectangle.rotate()
            for y in range(H - 1):
                rectangle.y = y
                rotated_rectangle.y = y
                for x in range(W - 1):
                    rectangle.x = x
                    rotated_rectangle.x = x

                    if rectangle.intersection_in_list(temp_layout) is None and rectangle.can_fit(W, H):
                        temp_layout.append(rectangle)
                        added = True
                        break
                    elif rotated_rectangle.intersection_in_list(temp_layout) is None and rotated_rectangle.can_fit(W, H):
                        temp_layout.append(rotated_rectangle)
                        added = True
                        break
                
                if added:
                    break
            
            if not added:
                rectangle.x = None
                rectangle.y = None
        
        if len(temp_layout) == len(rectangles):
            placed_rectangles = copy.deepcopy(temp_layout)
            break
        if len(temp_layout) >= len(placed_rectangles) and sum(rect.area() for rect in temp_layout) > sum(rect.area() for rect in placed_rectangles):
            placed_rectangles = copy.deepcopy(temp_layout)

    return [rect for rect in placed_rectangles if rect.x is not None and rect.y is not None]
    
