from tkinter import Canvas

from objet.forme import Forme

class Rectangle(Forme):
    
    def __init__(self, index: int, width: int, height: int) -> None:
        super().__init__(index)
        
        self._width: int = width
        self._height: int = height

    def __str__(self) -> str:
        return f"Rectangle[x={self.x}, y={self.y}, w={self.width}, h={self.height}]"
    
    def __repr__(self) -> str:
        return f"Rectangle[w={self.width}, h={self.height}]"
        
    def _get_width(self) -> int:
        return self._width
    
    def _set_width(self, width: int) -> None:
        self._width = width
        
    def _get_height(self) -> int:
        return self._height
    
    def _set_height(self, height: int) -> None:
        self._height = height
        
        
    width = property(_get_width, _set_width)
    height = property(_get_height, _set_height)

    def draw(self, canvas: Canvas):
        self.canvas_id = canvas.create_rectangle(self.x, self.y, self.x+self.width, self.y+self.height, fill = self.color, outline="black")
        self.text_id = canvas.create_text(self.x + self.width/2, self.y + self.height/2, text=str(self.index), font=("Helvetica", 12))

    def can_fit_on_side(self, new_rect, W, H, side) -> bool:
        match side:
            case "right":
                return (self.x + self.width + new_rect.width <= W)
            case "left":
                return (self.x - new_rect.width >= 0)
    
    def can_fit_under(self, new_rect, W, H) -> bool:
        return (self.y + self.height + new_rect.height <= H)
    
    def can_fit_above(self, new_rect, W, H) -> bool:
        return (self.x + new_rect.width <= H and self.y - new_rect.height <= H)
    
    def side_ok(self, other_rectangles) -> bool:
        for rect in other_rectangles:
            if (rect.x == self.x + self.width or rect.x == self.x - rect.width):
                return False
        return True
    
    def bottom_ok(self, other_rectangles) -> bool:
        for rect in other_rectangles:
            if rect.y == self.y + self.height:
                return False
        return True
    
    def top_ok(self, other_rectangles) -> bool:
        for rect in other_rectangles:
            if rect.x == self.x and rect.y == self.y - rect.height:
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
    
    def intersection_in_list(self, rectangles):
        for rectangle in rectangles:
            if rectangle.is_placed() and Rectangle.rectangles_intersect(self, rectangle):
                return rectangle
            
        return None