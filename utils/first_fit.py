from objet.rectangle import Rectangle

def first_fit_dh(rectangles, W, H):
    print(f"width:{W} and height:{H}")
    rectangles = [rect for rect in rectangles if rect.width <= W and rect.height <= H]
    rectangles.sort(key=lambda r: r.height, reverse=True)

    for rect in rectangles:
        rect.x = None
        rect.y = None

    rows = {}

    for rectangle in rectangles:
        if len(rows) == 0:
            first_row = Rectangle(rectangle.index, W, rectangle.height)
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
                new_row = Rectangle(rectangle.index, W, rectangle.height)
                new_row.x = 0
                new_row.y = H - occupied_height - rectangle.height

                rectangle.x = 0
                rectangle.y = H - occupied_height - rectangle.height
                rows[new_row] = [rectangle]
                

    return [rect for rect in rectangles if rect.x is not None and rect.y is not None]