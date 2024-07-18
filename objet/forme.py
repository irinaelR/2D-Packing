from abc import ABC, abstractmethod
import random

from tkinter import Canvas

class Forme(ABC):
    
    def __init__(self, index) -> None:  
        self._index = index
        
        self._x: int = None
        self._y: int = None
        
        self.coords: list = list()
        
        self._canvas_id: int = None
        self._text_id: int = None
        self._color: str = Forme.random_color_generator()
        
    def _get_index(self) -> int:
        return self._index
    
    def _set_index(self, index: int) -> None:
        self._index = index
        
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
        
    index: int = property(_get_index, _set_index)
    x: int = property(_get_x, _set_x)
    y: int = property(_get_y, _set_y)
    canvas_id: int = property(_get_canvas_id, _set_canvas_id)
    text_id: int = property(_get_text_id, _set_text_id)
    color: str = property(_get_color, _set_color)
            
    @staticmethod
    def random_color_generator():
        return "#"+''.join([random.choice('0123456789ABCDEF') for _ in range(6)])

    def draw(self, canvas: Canvas):
        coords = list(self.coords)
        self.canvas_id = canvas.create_polygon(coords, fill = self.color, outline="black")
        # center_x = (self.X[0] + self.X[1] + self.X[2]) / 3
        # center_y = (self.Y[0] + self.Y[1] + self.Y[2]) / 3
        # self.text_id = canvas.create_text(center_x, center_y, text=str(self.index), font=("Helvetica", 12))
    
    def undraw(self, canvas: Canvas):
        if self.canvas_id:
            canvas.delete(self.canvas_id)
            self.canvas_id = None
        if self.text_id:
            canvas.delete(self.text_id)
            self.text_id = None