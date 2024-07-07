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
    
    return [rect for rect in rectangles if rect.x is not None and rect.y is not None]