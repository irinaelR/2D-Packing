from tkinter import * # type: ignore

from utils.utilitaire import Utilitaire
from objet.forme import Forme

class Conteneur(Frame):
    
    def __init__(self, master = None, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._canvas = None        
        self.canvas_width: int = None
        self.canvas_height: int = None
        
        self._formes: list[Forme] = []
        
        self.formes_fitted: list[Forme] = []
        
        self.fit_chosen: str = None
        
    def _get_canvas(self) -> Canvas:
        return self._canvas
    
    def _set_canvas(self, canvas: Canvas) -> None:
        self._canvas = canvas
        
    def _get_formes(self) -> list[Forme]:
        return self._formes
    
    def _set_formes(self, formes: list[Forme]) -> None:
        self._formes = formes
        
        
    canvas: Canvas = property(_get_canvas, _set_canvas)
    formes: list[Forme] = property(_get_formes, _set_formes)
        
    def create_canvas(self, W, H):
        for widget in self.winfo_children():
            widget.destroy()

        self.canvas = Canvas(self, width=W, height=H, bg="white", highlightthickness=0)
        self.canvas.place(relx=0.5, rely=0.5, anchor="center")
        
    def add_forme(self, rect: Forme):
        self.formes.append(rect)
        
    def choose_fit(self, fit, form_temp, form_fitted_temp):
        for form in self.formes_fitted:
            form.undraw(self.canvas)
            
        self.fit_chosen = fit
        formes_fitted_temp = Utilitaire.choose_fit(self.fit_chosen, self.formes, int(self.canvas.cget('width')), int(self.canvas.cget('height')))
        self.formes_fitted = Utilitaire.polygon_to_canvas_element(formes_fitted_temp)
        
        print(f"Longueur de fitted {self.formes_fitted}")
        
        for form in self.formes_fitted:
            form.draw(self.canvas)
        
        form_temp[:] = self.formes
        form_fitted_temp[:] = self.formes_fitted
        
    def reset_formes(self):
        for form in self.formes_fitted:
            form.undraw(self.canvas)
            
        self.formes_fitted = []
        self.formes = []