import itertools

def brute_force_2(rectangles, W, H):
    rectangles = [rect for rect in rectangles if rect.width <= W and rect.height <= H]

    for rect in rectangles:
        rect.x = None
        rect.y = None

    placed_rectangles = []
    
    for permutation in itertools.permutations(rectangles):
        temp_layout = []
        
        for rectangle in permutation:
            added = False
            for i in range(W - rectangle.width + 1):
                rectangle.x = i
                for j in range(H - rectangle.height + 1):
                    rectangle.y = j
                    
                    if rectangle.intersection_in_list(temp_layout) is None:
                        temp_layout.append(rectangle)
                        added = True
                        break
                
                if added:
                    break
            
            if not added:
                rectangle.x = None
                rectangle.y = None

        if len(temp_layout) >= len(placed_rectangles):
            placed_rectangles = temp_layout

    return [rect for rect in placed_rectangles if rect.x is not None and rect.y is not None]

def brute_force(rectangles, W, H):
    rectangles = [rect for rect in rectangles if rect.width <= W and rect.height <= H]
    # rectangles.sort(key=lambda r: r.height, reverse=True)

    for rect in rectangles:
        rect.x = None
        rect.y = None

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
                lowest_rectangle = max(actual_layout, key=lambda rect: rect.y)
                next_y = lowest_rectangle.y + lowest_rectangle.height

                # round = 1
                # while round <= 2 and added is False:
                for placed_rect in actual_layout:

                    if placed_rect.side_ok(actual_layout) and placed_rect.can_fit_on_side(rectangle, W, H, "right"):
                        rectangle.x = placed_rect.x + placed_rect.width
                        for temp_y in range(H-rectangle.height+1):
                            rectangle.y = temp_y
                            # if the rectangle can be placed next to placed_rect WITHOUT overlapping any other
                            if rectangle.intersection_in_list(temp_layout) is None and temp_y + rectangle.height <= H:
                                count_placed += 1
                                added = True
                                break
                        if added:
                            break

                    elif placed_rect.bottom_ok(actual_layout) and placed_rect.can_fit_under(rectangle, W, H):
                        rectangle.y = placed_rect.y + placed_rect.height
                        for temp_x in range(W-rectangle.width+1):
                            rectangle.x = temp_x
                            # if the rectangle can be placed next to rect_in_list WITHOUT overlapping any other
                            if rectangle.intersection_in_list(temp_layout) is None and temp_x + rectangle.width <= W:
                                count_placed += 1
                                added = True
                                break
                        if added:
                            break

                    # round += 1
                
                if not added:
                    if next_y + rectangle.height <= H:
                        rectangle.x = 0
                        rectangle.y = next_y
                        count_placed += 1
                    else:
                        rectangle.x = None
                        rectangle.y = None

                temp_layout.append(rectangle)

        if max_placed_rectangles <= count_placed:
            # print(f"Went from {max_placed_rectangles} rectangles to {count_placed}")
            max_placed_rectangles = count_placed
            placed_rectangles = temp_layout
            insertion_order = permutation

    print(f"Permutation finale: {insertion_order}")

    return [rect for rect in placed_rectangles if rect.x is not None and rect.y is not None]