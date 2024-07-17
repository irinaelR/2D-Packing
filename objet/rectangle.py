import random
from tkinter import Canvas

class Rectangle:
    
    def __init__(self, index: int, width: int, height: int) -> None:
        self._width: int = width
        self._height: int = height
        self._index: int = index
        self._x: int = None
        self._y: int = None
        self._canvas_id: int = None
        self._text_id: int = None
        self._color: str = Rectangle.random_color_generator()
        
    def __str__(self) -> str:
        return f"Rectangle[x={self.x}, y={self.y}, w={self.width}, h={self.height}]"
    
    def __repr__(self) -> str:
        return f"Rectangle[index={self.index}, w={self.width}, h={self.height}, x={self.x}, y={self.y}]"
        
    def _get_index(self) -> int:
        return self._index
    
    def _set_index(self, index: int) -> None:
        self._index = index
        
    def _get_width(self) -> int:
        return self._width
    
    def _set_width(self, width: int) -> None:
        self._width = width
        
    def _get_height(self) -> int:
        return self._height
    
    def _set_height(self, height: int) -> None:
        self._height = height
        
    def _get_x(self) -> int:
        return self._x
    
    def _set_x(self, x: int) -> None:
        self._x = x
        
    def _get_y(self) -> int:
        return self._y
    
    def _set_y(self, y: int) -> None:
        self._y = y
        
    def _get_canvas_id(self) -> int:
        return self._canvas_id
    
    def _set_canvas_id(self, canvas_id: int) -> None:
        self._canvas_id = canvas_id
        
    def _get_text_id(self) -> int:
        return self._text_id
    
    def _set_text_id(self, text_id: int) -> None:
        self._text_id = text_id
        
    def _get_color(self) -> str:
        return self._color
    
    def _set_color(self, color: str) -> None:
        self._color = color
        
    width = property(_get_width, _set_width)
    height = property(_get_height, _set_height)
    index = property(_get_index, _set_index)
    x = property(_get_x, _set_x)
    y = property(_get_y, _set_y)
    canvas_id = property(_get_canvas_id, _set_canvas_id)
    text_id = property(_get_text_id, _set_text_id)
    color = property(_get_color, _set_color)
        
    @staticmethod
    def random_color_generator():
        return "#"+''.join([random.choice('0123456789ABCDEF') for _ in range(6)])

    def draw(self, canvas: Canvas):
        self.canvas_id = canvas.create_rectangle(self.x, self.y, self.x+self.width, self.y+self.height, fill = self.color, outline="black")
        self.text_id = canvas.create_text(self.x + self.width/2, self.y + self.height/2, text=str(self.index), font=("Helvetica", 12))
        
    def undraw(self, canvas: Canvas):
        if self.canvas_id:
            canvas.delete(self.canvas_id)
            self.canvas_id = None
        if self.text_id:
            canvas.delete(self.text_id)
            self.text_id = None

    def rotate(self):
        return Rectangle(self.index, self.height, self.width)
    
    def area(self):
        return self.width * self.height

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
            if rect.y == self.y and rect.x == self.x + self.width:
                return False
        return True
    
    def bottom_ok(self, other_rectangles) -> bool:
        occupied_width = 0
        for rect in other_rectangles:
            if rect.y == self.y + self.height:
                if rect.x <= self.x < (rect.x+rect.width):
                    occupied_width += rect.x + rect.width - self.x
                elif self.x <= rect.x < (self.x+self.width) and rect.x+rect.width <= self.x + self.width:
                    occupied_width += rect.width
                elif self.x <= rect.x < (self.x+self.width) and rect.x+rect.width > self.x + self.width:
                    occupied_width += self.x + self.width - rect.x
        return (occupied_width < self.width)
    
    def top_ok(self, other_rectangles) -> bool:
        for rect in other_rectangles:
            if rect.x == self.x and rect.y == self.y - rect.height:
                return False
        return True
    
    def is_placed(self) -> bool:
        return self.x != None and self.y != None
    
    def rectangles_intersect(rect1, rect2):
        # # Check if one rectangle is to the left of the other
        # if rect1.x + rect1.width <= rect2.x or rect2.x + rect2.width <= rect1.x:
        #     return False
        
        # # Check if one rectangle is above the other
        # if rect1.y + rect1.height <= rect2.y or rect2.y + rect2.height <= rect1.y:
        #     return False
        
        # return True
        if rect1.width == rect2.width and rect1.height == rect2.height and rect1.x == rect2.x and rect1.y == rect2.y:
            return True
        
        # elif rect1.x <= rect2.x < rect1.x + rect1.width or rect1.y <= rect2.y < rect1.y + rect1.height:
        #     return True
        # else:
        #     return False
        rectangle_points = [(rect1.x, rect1.y), (rect1.x + rect1.width, rect1.y), (rect1.x, rect1.y + rect1.height), (rect1.x + rect1.width, rect1.y + rect1.height), (rect1.x + int(rect1.width/2), rect1.y), (rect1.x + int(rect1.width/2), rect1.y + rect1.height), (rect1.x, rect1.y + int(rect1.height / 2)), (rect1.x + rect1.width, rect1.y + int(rect1.height / 2))]
        for point in rectangle_points:
            # if (rect2.x < point[0] < rect2.x + rect2.width and rect2.y <= point[1] < rect2.y + rect2.height) or (rect2.x <= point[0] < rect2.x + rect2.width and rect2.y < point[1] < rect2.y + rect2.height):
            #     return True
            if rect2.x < point[0] < rect2.x + rect2.width and rect2.y < point[1] < rect2.y + rect2.height:
                return True
        return False
        
    
    def intersection_in_list(self, rectangles):
        for rectangle in rectangles:
            if self.index == rectangle.index:
                continue
            if rectangle.is_placed() and (Rectangle.rectangles_intersect(self, rectangle) or Rectangle.rectangles_intersect(rectangle, self)):
                return rectangle
            
        return None
    
    def can_fit(self, W, H):
        return self.x + self.width <= W and self.y + self.height <= H