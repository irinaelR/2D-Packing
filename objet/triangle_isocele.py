from tkinter import Canvas
from objet.forme import Forme


class TriangleIsocele(Forme):
    
    def __init__(self, index: int, base: int, hauteur: int) -> None:
        super().__init__(index)
        
        self._base = base 
        self._hauteur = hauteur
        
        self._icks = []
        self._igrek = []
        
    def __str__(self) -> str:
        return f"Triangle[base={self.base}, hauteur={self.hauteur}]"
        
    def __repr__(self) -> str:
        return f"Triangle[base={self.base}, hauteur={self.hauteur}]"
        
    def _get_base(self) -> int:
        return self._base
    
    def _set_base(self, base: int) -> None:
        self._base = base
        
    def _get_hauteur(self) -> int:
        return self._hauteur
    
    def _set_hauteur(self, hauteur: int) -> None:
        self._hauteur = hauteur
        
    def _get_icks(self) -> list[int]:
        return self._icks
    
    def _set_icks(self, icks: list[int]) -> None:
        self._icks = icks
        
    def _get_igrek(self) -> list[int]:
        return self._igrek
    
    def _set_igrek(self, igrek: list[int]) -> None:
        self._igrek = igrek
        
    base = property(_get_base, _set_base)
    hauteur = property(_get_hauteur, _set_hauteur)
    icks = property(_get_icks, _set_icks)
    igrek = property(_get_igrek, _set_igrek)
    
    def draw(self, canvas: Canvas):
        self.canvas_id = canvas.create_polygon(self.icks[0], self.igrek[0], self.icks[1], self.igrek[1], self.icks[2], self.igrek[2], fill = self.color, outline="black")
        center_x = (self.icks[0] + self.icks[1] + self.icks[2]) / 3
        center_y = (self.igrek[0] + self.igrek[1] + self.igrek[2]) / 3
        self.text_id = canvas.create_text(center_x, center_y, text=str(self.index), font=("Helvetica", 12))