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
    return [rect for rect in placed_rectangles if rect.x is not None and rect.y is not None]

import copy
def brute_force_2(rectangles, W, H):
    rectangles = [rect for rect in rectangles if rect.width <= W and rect.height <= H]

    for rect in rectangles:
        rect.x = None
        rect.y = None

    placed_rectangles = []
    
    for permutation in itertools.permutations(rectangles):
        temp_layout = []
        # print(f"new perm: {permutation}")
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

        if len(temp_layout) >= len(placed_rectangles) and sum(rect.area() for rect in temp_layout) > sum(rect.area() for rect in placed_rectangles):
            placed_rectangles = copy.deepcopy(temp_layout)
            # print(f"{placed_rectangles} is the new placement with area of {sum(rect.area() for rect in placed_rectangles)}")

    return [rect for rect in placed_rectangles if rect.x is not None and rect.y is not None]

