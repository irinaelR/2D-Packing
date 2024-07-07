from tkinter import *  # type: ignore

from fenetrage.conteneur import Conteneur
from fenetrage.liste import Liste
from fenetrage.formulaire import Formulaire
from fenetrage.statistique import Statistique

class Fenetre(Tk):
    
    WIDTH: int = 1200
    HEIGHT: int = 650
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title("2D packing sans rotation")
        self.resizable(False, False) 

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x_cordinate = int((screen_width/2) - (self.WIDTH/2))
        y_cordinate = int((screen_height/2) - (self.HEIGHT/2))-30

        self.geometry("{}x{}+{}+{}".format(self.WIDTH, self.HEIGHT, x_cordinate, y_cordinate))        
        
        conteneur = Conteneur(self, bg = '#dbdbdb', width=900, height=550)
        liste = Liste(self, width=300, height=550)
        statistique = Statistique(self, width=300, height=100)
        
        formulaire = Formulaire(self, conteneur.create_canvas, conteneur.add_rectangle, liste.add_rectangle, conteneur.choose_fit, statistique.define_conteneur, statistique.define_rect, width=900, height=100)
        formulaire.initialize()
        formulaire.place(x=0, y=0)
        
        statistique.initialize()
        statistique.place(x=900, y=0)
        
        conteneur.pack(side="left", anchor=SW)
        
        liste.initialize()
        liste.pack(side="right", anchor=SE)
        
        


