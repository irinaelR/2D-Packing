import itertools

def brute_force(rectangles, W, H):
    rectangles = [rect for rect in rectangles if rect.width <= W and rect.height <= H]

    for rect in rectangles:
        rect.x = None
        rect.y = None

    placed_rectangles = []
    max_placed_rectangles = 0
    # insertion_order = None

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
                round = 1
                while round <= 2 and added is False:
                    for placed_rect in actual_layout:
                        if round == 1 and placed_rect.y + placed_rect.height > next_y:
                            next_y = placed_rect.y + placed_rect.height

                        if round == 1 and placed_rect.side_ok(actual_layout) and placed_rect.can_fit_on_side(rectangle, W, H):
                            rectangle.x = placed_rect.x + placed_rect.width
                            rectangle.y = placed_rect.y

                            # if the rectangle can be placed next to placed_rect WITHOUT overlapping any other
                            if not rectangle.has_intersection_in_list(temp_layout):
                                count_placed += 1
                                added = True
                                break

                        elif round == 2 and placed_rect.bottom_ok(actual_layout) and placed_rect.can_fit_under(rectangle, W, H):
                            rectangle.x = placed_rect.x
                            rectangle.y = placed_rect.y + placed_rect.height

                            # if the rectangle can be placed next to rect_in_list WITHOUT overlapping any other
                            if not rectangle.has_intersection_in_list(temp_layout):
                                count_placed += 1
                                added = True
                                break

                    round += 1
                
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
            # print(f"Went from {max_placed_rectangles} rectangles to {count_placed}")
            max_placed_rectangles = count_placed
            placed_rectangles = temp_layout
            # insertion_order = permutation

    return [rect for rect in placed_rectangles if rect.x is not None and rect.y is not None]

# def brute_force(rectangles, W, H):
#     placed_rectangles = []
#     max_placed_rectangles = 0
#     insertion_order = None

#     for permutation in itertools.permutations(rectangles):
#         temp_layout = []
#         count_placed = 0

#         for rectangle in permutation:
#             actual_layout = [rect for rect in temp_layout if rect.x is not None and rect.y is not None]
#             if len(actual_layout) == 0:
#                 rectangle.x = 0
#                 rectangle.y = 0
#                 temp_layout.append(rectangle)
#                 count_placed += 1
#             else:
#                 added = False
#                 next_y = -1
#                 for placed_rect in actual_layout:
#                     if placed_rect.y + placed_rect.height > next_y:
#                         next_y = placed_rect.y + placed_rect.height

#                     if placed_rect.side_ok(actual_layout) and placed_rect.can_fit_on_side(rectangle, W, H):
#                         rectangle.x = placed_rect.x + placed_rect.width
#                         rectangle.y = placed_rect.y

#                         # if the rectangle can be placed next to rect_in_list WITHOUT overlapping any other
#                         if not rectangle.has_intersection_in_list(temp_layout):
#                             count_placed += 1
#                             added = True
#                             break

#                     elif placed_rect.bottom_ok(actual_layout) and placed_rect.can_fit_under(rectangle, W, H):
#                         rectangle.x = placed_rect.x
#                         rectangle.y = placed_rect.y + placed_rect.height

#                         # if the rectangle can be placed next to rect_in_list WITHOUT overlapping any other
#                         if not rectangle.has_intersection_in_list(temp_layout):
#                             count_placed += 1
#                             added = True
#                             break
                
#                 if not added:
#                     if next_y + rectangle.height <= H and rectangle.width <= W:
#                         rectangle.x = 0
#                         rectangle.y = next_y
#                         count_placed += 1
#                     else:
#                         rectangle.x = None
#                         rectangle.y = None

#                 temp_layout.append(rectangle)

#         if max_placed_rectangles <= count_placed:
#             max_placed_rectangles = count_placed
#             placed_rectangles = temp_layout
#             insertion_order = permutation

#     return placed_rectangles, insertion_order
