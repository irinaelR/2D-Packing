class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = None
        self.y = None

    def __str__(self) -> str:
        return f"Rectangle[x={self.x}, y={self.y}, w={self.width}, h={self.height}]"
    
    def __repr__(self) -> str:
        return f"Rectangle[w={self.width}, h={self.height}]"

    def can_fit_on_side(self, new_rect, W, H) -> bool:
        return (self.x + self.width + new_rect.width <= W and self.y + new_rect.height <= H)
    
    def can_fit_under(self, new_rect, W, H) -> bool:
        return (self.x + new_rect.width <= W and self.y + self.height + new_rect.height <= H)
    
    def side_ok(self, other_rectangles) -> bool:
        for rect in other_rectangles:
            if rect.x == self.x + self.width and rect.y == self.y:
                return False
        return True
    
    def bottom_ok(self, other_rectangles) -> bool:
        for rect in other_rectangles:
            if rect.x == self.x and rect.y == self.y + self.height:
                return False
        return True
    
    def is_placed(self) -> bool:
        return self.x != None and self.y != None
    
    def rectangles_intersect(rect1, rect2):
        # Check if one rectangle is to the left of the other
        if rect1.x + rect1.width <= rect2.x or rect2.x + rect2.width <= rect1.x:
            return False
        
        # Check if one rectangle is above the other
        if rect1.y + rect1.height <= rect2.y or rect2.y + rect2.height <= rect1.y:
            return False
        
        return True
    
    def has_intersection_in_list(self, rectangles) -> bool:
        for rectangle in rectangles:
            if rectangle.is_placed() and Rectangle.rectangles_intersect(self, rectangle):
                return True
            
        return False


def next_fit_dh(rectangles, W, H):
    rectangles.sort(key=lambda r: r.height, reverse=True)
    
    current_row = None
    current_row_rect = []
    occupied_height = 0

    for rectangle in rectangles:
        if current_row == None:
            # first row
            current_row = Rectangle(W, rectangle.height)

            current_row.x = 0
            current_row.y = H - rectangle.height
            
            occupied_height = occupied_height + rectangle.height

        occupied_width = 0
        for placed_rect in current_row_rect:
            occupied_width = occupied_width + placed_rect.width

        if occupied_width + rectangle.width <= W:
            # can fit into the current row, we append
            rectangle.y = current_row.y
            rectangle.x = occupied_width
            current_row_rect.append(rectangle)

        elif occupied_height + rectangle.height <= H:
            # new row
            current_row = Rectangle(W, rectangle.height)

            current_row.x = 0
            current_row.y = H - rectangle.height - occupied_height

            rectangle.x = current_row.x
            rectangle.y = current_row.y

            current_row_rect = [rectangle]

            occupied_height = occupied_height + rectangle.height

    return rectangles

def first_fit_dh(rectangles, W, H):
    rectangles.sort(key=lambda r: r.height, reverse=True)

    rows = {}

    for rectangle in rectangles:
        if rectangle.height <= H:
            if len(rows) == 0:
                first_row = Rectangle(W, rectangle.height)
                first_row.x = 0
                first_row.y = H - rectangle.height

                rectangle.x = 0
                rectangle.y = H - rectangle.height

                rows[first_row] = [rectangle]
            else:
                added = False
                occupied_height = 0
                for row in rows:
                    # the height of a row is defined by the height of its key
                    occupied_height = occupied_height + row.height

                    row_rectangles = rows[row]
                    occupied_width = 0
                    for r in row_rectangles:
                        occupied_width = occupied_width + r.width
                    
                    if occupied_width + rectangle.width <= W:
                        # if there is still horizontal space
                        rectangle.x  = occupied_width
                        rectangle.y = row.y

                        rows[row].append(rectangle)
                        added = True
                        break
                
                if not added and occupied_height + rectangle.height <= H:
                    # we'll try to make a new row
                    new_row = Rectangle(W, rectangle.height)
                    new_row.x = 0
                    new_row.y = H - occupied_height - rectangle.height

                    rectangle.x = 0
                    rectangle.y = H - occupied_height - rectangle.height
                    rows[new_row] = [rectangle]
                

    return rectangles

def best_fit(rectangles, W, H):
    rectangles.sort(key=lambda r: r.height, reverse=True)

    free_spaces = [(0, 0, W, H)]

    for rect in rectangles:
        best_space = None
        min_waste = float('inf')
        
        for space in free_spaces:
            sx, sy, sw, sh = space
            if rect.width <= sw and rect.height <= sh:
                waste = (sw - rect.width) * (sh - rect.height)
                if waste < min_waste:
                    min_waste = waste
                    best_space = space
        
        if best_space:
            sx, sy, sw, sh = best_space
            rect.x, rect.y = sx, sy

            free_spaces.remove(best_space)
            new_spaces = [
                (sx + rect.width, sy, sw - rect.width, rect.height),
                (sx, sy + rect.height, sw, sh - rect.height)
            ]
            
            valid_new_spaces = []
            for new_space in new_spaces:
                nsx, nsy, nsw, nsh = new_space
                if nsw > 0 and nsh > 0:
                    valid_new_spaces.append(new_space)
            free_spaces.extend(valid_new_spaces)
    
    return rectangles

import itertools

def brute_force(rectangles, W, H):
    placed_rectangles = []
    max_placed_rectangles = 0
    insertion_order = None

    for permutation in itertools.permutations(rectangles):
        temp_layout = []
        count_placed = 0

        for rectangle in permutation:
            actual_layout = [rect for rect in temp_layout if rect.x is not None and rect.y is not None]
            if len(actual_layout) == 0:
                rectangle.x = 0
                rectangle.y = 0
                temp_layout.append(rectangle)
                count_placed += 1
            else:
                added = False
                next_y = -1
                for placed_rect in actual_layout:
                    if placed_rect.y + placed_rect.height > next_y:
                        next_y = placed_rect.y + placed_rect.height

                    if placed_rect.side_ok(actual_layout) and placed_rect.can_fit_on_side(rectangle, W, H):
                        rectangle.x = placed_rect.x + placed_rect.width
                        rectangle.y = placed_rect.y

                        # if the rectangle can be placed next to rect_in_list WITHOUT overlapping any other
                        if not rectangle.has_intersection_in_list(temp_layout):
                            count_placed += 1
                            added = True
                            break

                    elif placed_rect.bottom_ok(actual_layout) and placed_rect.can_fit_under(rectangle, W, H):
                        rectangle.x = placed_rect.x
                        rectangle.y = placed_rect.y + placed_rect.height

                        # if the rectangle can be placed next to rect_in_list WITHOUT overlapping any other
                        if not rectangle.has_intersection_in_list(temp_layout):
                            count_placed += 1
                            added = True
                            break
                
                if not added:
                    if next_y + rectangle.height <= H and rectangle.width <= W:
                        rectangle.x = 0
                        rectangle.y = next_y
                        count_placed += 1
                    else:
                        rectangle.x = None
                        rectangle.y = None

                temp_layout.append(rectangle)

        if max_placed_rectangles <= count_placed:
            max_placed_rectangles = count_placed
            placed_rectangles = temp_layout
            insertion_order = permutation

    return placed_rectangles, insertion_order

# /!\ DOESN'T WORK YET
def brute_force_with_rotation(rectangles, W, H):
    placed_rectangles = []
    max_placed_rectangles = 0
    insertion_order = None

    for permutation in itertools.permutations(rectangles):
        # print(permutation)
        temp_layout = []
        count_placed = 0

        for rectangle in permutation:
            actual_layout = [rect for rect in temp_layout if rect.x is not None and rect.y is not None]
            if len(actual_layout) == 0:
                rectangle.x = 0
                rectangle.y = 0
                temp_layout.append(rectangle)
                count_placed += 1
            else:
                added = False
                next_y = -1
                for placed_rect in actual_layout:
                    if placed_rect.y + placed_rect.height > next_y:
                        next_y = placed_rect.y + placed_rect.height

                    if placed_rect.side_ok(actual_layout) and placed_rect.can_fit_on_side(rectangle, W, H):
                        rectangle.x = placed_rect.x + placed_rect.width
                        rectangle.y = placed_rect.y

                        # if the rectangle can be placed next to rect_in_list WITHOUT overlapping any other
                        if not rectangle.has_intersection_in_list(temp_layout):
                            count_placed += 1
                            added = True
                            break

                    elif placed_rect.side_ok(actual_layout) and placed_rect.can_fit_on_side(Rectangle(rectangle.height, rectangle.width), W, H):
                        # print('a rotation happened')
                        rectangle = Rectangle(rectangle.height, rectangle.width)
                        rectangle.x = placed_rect.x + placed_rect.width
                        rectangle.y = placed_rect.y

                        # if the rectangle can be placed next to rect_in_list WITHOUT overlapping any other
                        if not rectangle.has_intersection_in_list(temp_layout):
                            count_placed += 1
                            added = True
                            break

                    elif placed_rect.bottom_ok(actual_layout) and placed_rect.can_fit_under(rectangle, W, H):
                        rectangle.x = placed_rect.x
                        rectangle.y = placed_rect.y + placed_rect.height

                        # if the rectangle can be placed next to rect_in_list WITHOUT overlapping any other
                        if not rectangle.has_intersection_in_list(temp_layout):
                            count_placed += 1
                            added = True
                            break

                    elif placed_rect.bottom_ok(actual_layout) and placed_rect.can_fit_under(Rectangle(rectangle.height, rectangle.width), W, H):
                        # print('a rotation happened')
                        
                        rectangle = Rectangle(rectangle.height, rectangle.width)
                        rectangle.x = placed_rect.x
                        rectangle.y = placed_rect.y + placed_rect.height

                        # if the rectangle can be placed next to rect_in_list WITHOUT overlapping any other
                        if not rectangle.has_intersection_in_list(temp_layout):
                            count_placed += 1
                            added = True
                            break
                
                if not added:
                    if next_y + rectangle.height <= H and rectangle.width <= W:
                        rectangle.x = 0
                        rectangle.y = next_y
                        count_placed += 1

                    elif next_y + rectangle.width <= H and rectangle.height <= W:
                        rectangle = Rectangle(rectangle.height, rectangle.width)
                        rectangle.x = 0
                        rectangle.y = next_y
                        count_placed += 1

                    else:
                        rectangle.x = None
                        rectangle.y = None

                temp_layout.append(rectangle)

        if max_placed_rectangles <= count_placed:
            max_placed_rectangles = count_placed
            placed_rectangles = temp_layout
            insertion_order = permutation

    return placed_rectangles, insertion_order


rectangles = [Rectangle(4, 3), Rectangle(7, 4), Rectangle(4, 3), Rectangle(3, 3), Rectangle(2, 1), Rectangle(2, 8), Rectangle(10, 1)]
W, H = 10, 10

# rectangles = [Rectangle(3, 2), Rectangle(2, 2), Rectangle(5, 4)]
# W, H = 4, 3

# placed_rectangles = next_fit_dh(rectangles, W, H)
# print('Next fit decreasing height')
# for rect in placed_rectangles:
#     if rect.x is not None and rect.y is not None:
#         print(f'Rectangle at ({rect.x}, {rect.y}) with width {rect.width} and height {rect.height}')
#     else:
#         print(f'Rectangle with width {rect.width} and height {rect.height} could not be placed')


# placed_rectangles2 = first_fit_dh(rectangles, W, H)
# print('First fit')
# for rect in placed_rectangles2:
#     if rect.x is not None and rect.y is not None:
#         print(f'Rectangle at ({rect.x}, {rect.y}) with width {rect.width} and height {rect.height}')
#     else:
#         print(f'Rectangle with width {rect.width} and height {rect.height} could not be placed')

# placed_rectangles3 = best_fit(rectangles, W, H)
# print('Best fit')
# for rect in placed_rectangles3:
#     if rect.x is not None and rect.y is not None:
#         print(f'Rectangle at ({rect.x}, {rect.y}) with width {rect.width} and height {rect.height}')
#     else:
#         print(f'Rectangle with width {rect.width} and height {rect.height} could not be placed')

#         placed_rectangles3 = best_fit(rectangles, W, H)

placed_rectangles4, insertion_order = brute_force(rectangles, W, H)
print('Brute force')
print(insertion_order)
for rect in placed_rectangles4:
    if rect.x is not None and rect.y is not None:
        print(f'Rectangle at ({rect.x}, {rect.y}) with width {rect.width} and height {rect.height}')
    else:
        print(f'Rectangle with width {rect.width} and height {rect.height} could not be placed')

placed_rectangles4, insertion_order = brute_force_with_rotation(rectangles, W, H)
print('Brute force with rotation')
print(insertion_order)
for rect in placed_rectangles4:
    if rect.x is not None and rect.y is not None:
        print(f'Rectangle at ({rect.x}, {rect.y}) with width {rect.width} and height {rect.height}')
    else:
        print(f'Rectangle with width {rect.width} and height {rect.height} could not be placed')