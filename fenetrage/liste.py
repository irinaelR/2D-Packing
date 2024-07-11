import tkinter as tk
from tkinter import ttk

from objet.forme import Forme

class Liste(tk.Frame):
    
    WIDTH = 300
    HEIGHT = 400
    
    def __init__(self, master, reset_formes, reset=None, **kwargs) -> None:
        super().__init__(master, **kwargs)
        
        self.reset_formes = reset_formes
        self.reset_index = reset
        
        self._treeview = ttk.Treeview(self, columns = ('number', 'info'), show='headings', height=24)
        
        self.reset = tk.Button(self, text="RESET", command=self.reset_form)
        
        self._formes: list[Forme] = []
        
    def _get_treeview(self) -> ttk.Treeview:
        return self._treeview
    
    def _set_treeview(self, treeview: ttk.Treeview) -> None:
        self._treeview = treeview
        
    def _get_formes(self) -> list[Forme]:
        return self._formes
    
    def _set_formes(self, formes: list[Forme]) -> None:
        self._formes = formes
        
    treeview: ttk.Treeview = property(_get_treeview, _set_treeview)
    formes: list[Forme] = property(_get_formes, _set_formes)
    
    def initialize(self):
        self.treeview.column('number', anchor='center', stretch='no', width=100)
        self.treeview.heading('number', text='Number')
        self.treeview.column('info', anchor='center', stretch='no', width=200)
        self.treeview.heading('info', text='Info')
        self.treeview.grid(row=0)
        self.reset.grid(row=1, pady=10)
        
    def add_forme(self, form: Forme) -> None:
        self.formes.append(form)
        self.update_treeview()
        
    def update_treeview(self) -> None:
        for element in self.treeview.get_children():
            self.treeview.delete(element)

        for rect in self.formes:
            
            self.treeview.insert("", "end", values=(rect.index, repr(rect)))
            
    def reset_form(self):
        self.reset_formes()
        self.reset_index()
        self.formes = []
        
        for element in self.treeview.get_children():
            self.treeview.delete(element)