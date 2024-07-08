from tkinter import * # type: ignore

from objet.rectangle import Rectangle

class Statistique(Frame):
    
    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, **kwargs)
                
        self.conteneur: tuple = None
        self.rectangles: list[Rectangle] = None
        self.rectangles_fitted: list[Rectangle] = None
        
        self.surface_totale_label = Label(self, text="Surface totale:")
        self.surface_totale = Label(self)
        
        self.surface_occupee_label = Label(self, text="Surface occupée:")
        self.surface_occupee = Label(self)
        
        self.surface_restante_label = Label(self, text="Surface restante:")
        self.surface_restante = Label(self)
        
        self.rect_given_label = Label(self, text="Rectangles donnés:")
        self.rect_given = Label(self)
        
        self.rect_inserted_label = Label(self, text="Rectangles inserés:")
        self.rect_inserted = Label(self)
        
        
    def initialize(self) -> None:
        self.surface_totale_label.grid(row=0, column=0, columnspan=2, padx=10, pady=2, sticky="w")
        self.surface_totale.grid(row=0, column=1, columnspan=2, padx=10, pady=2)
        
        self.surface_occupee_label.grid(row=1, column=0, columnspan=2, padx=10, pady=2, sticky="w")
        self.surface_occupee.grid(row=1, column=1,columnspan=2, padx=10, pady=2)
        
        self.surface_restante_label.grid(row=2, column=0, columnspan=2, padx=10, pady=2, sticky="w")
        self.surface_restante.grid(row=2, column=1, columnspan=2, padx=10, pady=2)
        
        self.rect_given_label.grid(row=3, column=0, padx=10, pady=3)
        self.rect_given.grid(row=3, column=1)
        
        self.rect_inserted_label.grid(row=3, column=2, padx=10, pady=3)
        self.rect_inserted.grid(row=3, column=4)
        
    def define_conteneur(self, width, height) -> None:
        self.conteneur = (width, height)
        surface_totale = self.conteneur[0] * self.conteneur[1]
        self.surface_totale.config(text=f"{surface_totale:,}")
        
    def calcul_surface_rect(self, rect: list[Rectangle]):
        value = 0
        for rectangle in rect:
            temp = rectangle.width * rectangle.height
            value += temp
        return value
        
    def define_rect(self, rect, rect_fitted):
        self.rectangles = rect
        self.rectangles_fitted = rect_fitted

        occupee = self.calcul_surface_rect(self.rectangles_fitted)
        self.surface_occupee.config(text=f"{occupee:,}")
        
        surface_totale = self.conteneur[0] * self.conteneur[1]
        restante = surface_totale - occupee
        self.surface_restante.config(text=f"{restante:,}")
        
        self.rect_given.config(text=f"{len(self.rectangles)}")
        self.rect_inserted.config(text=f"{len(self.rectangles_fitted)}")
