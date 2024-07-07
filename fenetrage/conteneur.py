from tkinter import * # type: ignore

from utils.utilitaire import Utilitaire
from objet.rectangle import Rectangle

class Conteneur(Frame):
    
    def __init__(self, master = None, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._canvas = None        
        self.canvas_width: int = None
        self.canvas_height: int = None
        
        self._rectangles: list[Rectangle] = []
        
        self.rectangles_fitted: list[Rectangle] = []
        
        self.fit_chosen: str = None
        
    def _get_canvas(self) -> Canvas:
        return self._canvas
    
    def _set_canvas(self, canvas: Canvas) -> None:
        self._canvas = canvas
        
    def _get_rectangles(self) -> list[Rectangle]:
        return self._rectangles
    
    def _set_rectangles(self, rectangles: list[Rectangle]) -> None:
        self._rectangles = rectangles
        
        
    canvas: Canvas = property(_get_canvas, _set_canvas)
    rectangles: list[Rectangle] = property(_get_rectangles, _set_rectangles)
        
    def create_canvas(self, width, height):
        for widget in self.winfo_children():
            widget.destroy()

        self.canvas = Canvas(self, width=width, height=height, bg="white")
        self.canvas.place(relx=0.5, rely=0.5, anchor="center")
        
    def add_rectangle(self, rect: Rectangle):
        self.rectangles.append(rect)
        
    def choose_fit(self, fit, rect_temp, rect_fitted_temp):
        for rect in self.rectangles_fitted:
            print(rect)
            rect.undraw(self.canvas)
            
        self.fit_chosen = fit
        self.rectangles_fitted = Utilitaire.choose_fit(self.fit_chosen, self.rectangles, self.canvas.winfo_width(), self.canvas.winfo_height())
        
        for rect in self.rectangles_fitted:
            rect.draw(self.canvas)
        
        rect_temp[:] = self.rectangles
        rect_fitted_temp[:] = self.rectangles_fitted
            