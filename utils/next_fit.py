from objet.rectangle import Rectangle

def next_fit_dh(rectangles, W, H):
    rectangles = [rect for rect in rectangles if rect.width <= W and rect.height <= H]
    rectangles.sort(key=lambda r: r.height, reverse=True)
    
    current_row = None
    current_row_rect = []
    occupied_height = 0

    for rectangle in rectangles:
        if current_row == None:
            # first row
            current_row = Rectangle(rectangle.index, W, rectangle.height)

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
            current_row = Rectangle(rectangle.index, W, rectangle.height)

            current_row.x = 0
            current_row.y = H - rectangle.height - occupied_height

            rectangle.x = current_row.x
            rectangle.y = current_row.y

            current_row_rect = [rectangle]

            occupied_height = occupied_height + rectangle.height

    return [rect for rect in rectangles if rect.x is not None and rect.y is not None]