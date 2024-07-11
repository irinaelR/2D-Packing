from tkinter import Canvas
from objet.forme import Forme

class Cercle(Forme):
    
    def __init__(self, index: int, rayon: int) -> None:
        super().__init__(index)
        
        self._rayon = rayon
    
    def __str__(self) -> str:
        return f"Cercle[index={self.index}, rayon={self.rayon}]"
    
    def __repr__(self) -> str:
        return f"Cercle[rayon={self.rayon}]"
        
    def _get_rayon(self) -> int:
        return self._rayon
    
    def _set_rayon(self, rayon: int) -> None:
        self._rayon = rayon
        
    rayon = property(_get_rayon, _set_rayon)
        
    def draw(self, canvas: Canvas):
        self.canvas_id = canvas.create_oval(self.x, self.y, self.x+self.width, self.y+self.height, fill = self.color, outline="black")
        self.text_id = canvas.create_text(self.x + self.width/2, self.y + self.height/2, text=str(self.index), font=("Helvetica", 12))