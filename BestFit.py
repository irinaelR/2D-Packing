class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = None
        self.y = None

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

rectangles = [Rectangle(7, 5), Rectangle(5, 3), Rectangle(4, 3), Rectangle(3, 3), Rectangle(3, 2)]
W, H = 15, 11

# rectangles = [Rectangle(3, 2), Rectangle(2, 2), Rectangle(5, 4)]
# W, H = 4, 3

placed_rectangles = next_fit_dh(rectangles, W, H)
print('Next fit decreasing height')
for rect in placed_rectangles:
    if rect.x is not None and rect.y is not None:
        print(f'Rectangle at ({rect.x}, {rect.y}) with width {rect.width} and height {rect.height}')
    else:
        print(f'Rectangle with width {rect.width} and height {rect.height} could not be placed')


placed_rectangles2 = first_fit_dh(rectangles, W, H)
print('First fit')
for rect in placed_rectangles2:
    if rect.x is not None and rect.y is not None:
        print(f'Rectangle at ({rect.x}, {rect.y}) with width {rect.width} and height {rect.height}')
    else:
        print(f'Rectangle with width {rect.width} and height {rect.height} could not be placed')

placed_rectangles3 = best_fit(rectangles, W, H)
print('Best fit')
for rect in placed_rectangles2:
    if rect.x is not None and rect.y is not None:
        print(f'Rectangle at ({rect.x}, {rect.y}) with width {rect.width} and height {rect.height}')
    else:
        print(f'Rectangle with width {rect.width} and height {rect.height} could not be placed')