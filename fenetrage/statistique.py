from tkinter import * # type: ignore

from objet.forme import Forme

class Statistique(Frame):
    
    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, **kwargs)
                
        self.conteneur: tuple = None
        self.formes: list[Forme] = None
        self.formes_fitted: list[Forme] = None
        
        self.surface_totale_label = Label(self, text="Surface totale:")
        self.surface_totale = Label(self)
        
        self.surface_occupee_label = Label(self, text="Surface occupée:")
        self.surface_occupee = Label(self)
        
        self.surface_restante_label = Label(self, text="Surface restante:")
        self.surface_restante = Label(self)
        
        self.form_given_label = Label(self, text="Formes donnés:")
        self.form_given = Label(self)
        
        self.form_inserted_label = Label(self, text="Formes inserés:")
        self.form_inserted = Label(self)
        
        
    def initialize(self) -> None:
        self.surface_totale_label.grid(row=0, column=0, columnspan=2, padx=10, pady=2, sticky="w")
        self.surface_totale.grid(row=0, column=1, columnspan=2, padx=10, pady=2)
        
        self.surface_occupee_label.grid(row=1, column=0, columnspan=2, padx=10, pady=2, sticky="w")
        self.surface_occupee.grid(row=1, column=1,columnspan=2, padx=10, pady=2)
        
        self.surface_restante_label.grid(row=2, column=0, columnspan=2, padx=10, pady=2, sticky="w")
        self.surface_restante.grid(row=2, column=1, columnspan=2, padx=10, pady=2)
        
        self.form_given_label.grid(row=3, column=0, padx=10, pady=3)
        self.form_given.grid(row=3, column=1)
        
        self.form_inserted_label.grid(row=3, column=2, padx=10, pady=3)
        self.form_inserted.grid(row=3, column=4)
        
    def define_conteneur(self, width, height) -> None:
        self.conteneur = (width, height)
        surface_totale = self.conteneur[0] * self.conteneur[1]
        self.surface_totale.config(text=f"{surface_totale:,}")
        
    def calcul_surface_form(self, form: list[Forme]):
        value = 0
        for formangle in form:
            temp = formangle.width * formangle.height
            value += temp
        return value
        
    def define_form(self, form, form_fitted):
        self.formes = form
        self.formes_fitted = form_fitted

        # occupee = self.calcul_surface_form(self.formes_fitted)
        # self.surface_occupee.config(text=f"{occupee:,}")
        
        # surface_totale = self.conteneur[0] * self.conteneur[1]
        # restante = surface_totale - occupee
        # self.surface_restante.config(text=f"{restante:,}")
        
        # self.form_given.config(text=f"{len(self.formes)}")
        # self.form_inserted.config(text=f"{len(self.formes_fitted)}")
