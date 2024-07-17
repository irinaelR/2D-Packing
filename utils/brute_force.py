import itertools

def brute_force(rectangles, W, H):
    rectangles = [rect for rect in rectangles if rect.width <= W and rect.height <= H]

    for rect in rectangles:
        rect.x = None
        rect.y = None

    placed_rectangles = []
    permutation_finale = None

    # permutation = rectangles

    for permutation in itertools.permutations(rectangles):
        temp_layout = []
        first_row_closed = False

        current_reference = None
        references = []
        
        for index, rectangle in enumerate(permutation): #n!
            if len(temp_layout) == 0:
                rectangle.x = 0
                rectangle.y = 0
                temp_layout.append(rectangle)
                references.append(rectangle)
                current_reference = rectangle
            else:
                added = False
                # rectangle.x = current_reference.x + current_reference.width # à droite
                # for temp_y in range(current_reference.y, current_reference.y + current_reference.height + 1):
                #     rectangle.y = temp_y
                #     if rectangle.intersection_in_list(temp_layout) is None and rectangle.x + rectangle.width <= W:
                #         temp_layout.append(rectangle)
                #         references.append(rectangle)
                #         added = True
                #         break
                
                # if not added:
                #     rectangle.y = current_reference.y + current_reference.height
                #     for temp_x in range(current_reference.x, current_reference.x + current_reference.width):
                #         rectangle.x = temp_x
                #         if rectangle.intersection_in_list(temp_layout) is None and rectangle.y + rectangle.height <= H:
                #             temp_layout.append(rectangle)
                #             references.append(rectangle)
                #             added = True
                #             break
                if current_reference.side_ok(temp_layout) and current_reference.can_fit_on_side(rectangle, W, H, "right"):
                    rectangle.x = current_reference.x + current_reference.width
                    for temp_y in range(H - rectangle.height + 1):
                        rectangle.y = temp_y
                        # rectangle.y = current_reference.y
                        if rectangle.intersection_in_list(permutation) is None:
                            temp_layout.append(rectangle)
                            references.append(rectangle)
                            added = True
                            # print(f"place {rectangle} next to {current_reference}")
                            
                            break
                elif current_reference.bottom_ok(temp_layout) and current_reference.can_fit_under(rectangle, W, H):
                    rectangle.y = current_reference.y + current_reference.height
                    for temp_x in range(W - rectangle.width + 1):
                        rectangle.x = temp_x
                        if rectangle.intersection_in_list(permutation) is None:
                            temp_layout.append(rectangle)
                            references.append(rectangle)
                            added = True
                            # print(f"place {rectangle} under {current_reference}")

                            break

                if not added:
                    rectangle.x = None
                    rectangle.y = None
                    continue

                if not first_row_closed and rectangle.is_placed() and (rectangle.y > 0 or (index < len(permutation)-1 and not current_reference.can_fit_on_side(permutation[index+1], W, H, "right"))):
                    # print(f"{rectangle} cannot be a reference")
                    first_row_closed = True

                if not first_row_closed:
                    current_reference = rectangle
                    # print(f"{rectangle} is the new reference")
                    # first_row_closed = (index < len(permutation)-1 and (not current_reference.side_ok(temp_layout) or not current_reference.can_fit_on_side(permutation[index+1], W, H, "right")))
                elif index < len(permutation) - 1 and not (current_reference.can_fit_on_side(permutation[index+1], W, H, "right") and current_reference.side_ok(temp_layout)) and not (current_reference.can_fit_under(permutation[index+1], W, H) and current_reference.bottom_ok(temp_layout)):
                    # references.pop(0)
                    # current_reference = references[0]
                    # print(f"current reference = {current_reference}")
                    # print(f"next block = {permutation[index+1]}")
                    for ref in references:
                        if ((ref.side_ok(temp_layout) and ref.can_fit_on_side(permutation[index+1], W, H, "right")) or (ref.bottom_ok(temp_layout) and ref.can_fit_under(permutation[index+1], W, H))):
                            current_reference = ref
                            # print(f"{current_reference} is the new reference")
                            break
                        else:
                            pass
                            # print(f"{ref} could not be a reference")

        if len(temp_layout) == len(rectangles):
            placed_rectangles = temp_layout
            permutation_finale = permutation
            break
        elif len(placed_rectangles) < len(temp_layout):
            placed_rectangles = temp_layout
            permutation_finale = permutation

    # print(f"Permutation finale: {permutation_finale}")
    return [rect for rect in permutation_finale if rect.x is not None and rect.y is not None]


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

# def brute_force(rectangles, W, H):
#     rectangles = [rect for rect in rectangles if rect.width <= W and rect.height <= H]
#     # rectangles.sort(key=lambda r: r.height, reverse=True)

#     for rect in rectangles:
#         rect.x = None
#         rect.y = None

#     placed_rectangles = []
#     max_placed_rectangles = 0
#     insertion_order = None 

#     for permutation in itertools.permutations(rectangles):
#         temp_layout = []
#         count_placed = 0
#         reference = None

#         for rectangle in permutation:
#             actual_layout = [rect for rect in temp_layout if rect.x is not None and rect.y is not None]
#             if len(actual_layout) == 0:
#                 rectangle.x = 0
#                 rectangle.y = 0
#                 temp_layout.append(rectangle)
#                 count_placed += 1
#                 reference = rectangle
#             else:
#                 added = False
#                 lowest_rectangle = max(actual_layout, key=lambda rect: rect.y)
#                 next_y = lowest_rectangle.y + lowest_rectangle.height

#                 if reference.side_ok(actual_layout) and reference.can_fit_on_side(rectangle, W, H, "right"):
#                     rectangle.x = reference.x + reference.width
#                     for temp_y in range(H-rectangle.height+1):
#                         rectangle.y = temp_y
#                         # if the rectangle can be placed next to placed_rect WITHOUT overlapping any other
#                         if rectangle.intersection_in_list(temp_layout) is None and temp_y + rectangle.height <= H:
#                             count_placed += 1
#                             added = True
#                             reference = rectangle
#                 else:
#                     pass
#                     # reference = max([rect for rect in actual_layout if rect.x = 0], key=lambda rect: rect.y)
#                     # if reference.bottom_ok(actual_layout):
#                     #     pass



#                 # round = 1
#                 # while round <= 2 and added is False:
#                 for placed_rect in actual_layout:

#                     if placed_rect.side_ok(actual_layout) and placed_rect.can_fit_on_side(rectangle, W, H, "right"):
#                         rectangle.x = placed_rect.x + placed_rect.width
#                         for temp_y in range(H-rectangle.height+1):
#                             rectangle.y = temp_y
#                             # if the rectangle can be placed next to placed_rect WITHOUT overlapping any other
#                             if rectangle.intersection_in_list(temp_layout) is None and temp_y + rectangle.height <= H:
#                                 count_placed += 1
#                                 added = True
#                                 break
#                         if added:
#                             break

#                     elif placed_rect.bottom_ok(actual_layout) and placed_rect.can_fit_under(rectangle, W, H):
#                         rectangle.y = placed_rect.y + placed_rect.height
#                         for temp_x in range(W-rectangle.width+1):
#                             rectangle.x = temp_x
#                             # if the rectangle can be placed next to rect_in_list WITHOUT overlapping any other
#                             if rectangle.intersection_in_list(temp_layout) is None and temp_x + rectangle.width <= W:
#                                 count_placed += 1
#                                 added = True
#                                 break
#                         if added:
#                             break

#                     # round += 1
                
#                 if not added:
#                     if next_y + rectangle.height <= H:
#                         rectangle.x = 0
#                         rectangle.y = next_y
#                         count_placed += 1
#                     else:
#                         rectangle.x = None
#                         rectangle.y = None

#                 temp_layout.append(rectangle)

#         if max_placed_rectangles < count_placed:
#             # print(f"Went from {max_placed_rectangles} rectangles to {count_placed}")
#             max_placed_rectangles = count_placed
#             placed_rectangles = temp_layout
#             insertion_order = permutation

#     print(f"Permutation finale: {insertion_order}")

#     return [rect for rect in placed_rectangles if rect.x is not None and rect.y is not None]