import tkinter as tk
from tkinter import ttk

from objet.rectangle import Rectangle

class Liste(tk.Frame):
    
    WIDTH = 300
    HEIGHT = 400
    
    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, **kwargs)
        
        self._treeview = ttk.Treeview(self, columns = ('number', 'width', 'height'), show='headings', height=26)
        
        self._rectangles: list[Rectangle] = []
        
    def _get_treeview(self) -> ttk.Treeview:
        return self._treeview
    
    def _set_treeview(self, treeview: ttk.Treeview) -> None:
        self._treeview = treeview
        
    def _get_rectangles(self) -> list[Rectangle]:
        return self._rectangles
    
    def _set_rectangles(self, rectangles: list[Rectangle]) -> None:
        self._rectangles = rectangles
        
    treeview: ttk.Treeview = property(_get_treeview, _set_treeview)
    rectangles: list[Rectangle] = property(_get_rectangles, _set_rectangles)
    
    def initialize(self):
        self.treeview.column('number', anchor='center', stretch='no', width=100)
        self.treeview.heading('number', text='Number')
        self.treeview.column('width', anchor='center', stretch='no', width=100)
        self.treeview.heading('width', text='Width')
        self.treeview.column('height', anchor='center', stretch='no', width=100)
        self.treeview.heading('height', text='Height')
        self.treeview.place(relx=0.5, rely=0.5, anchor='center')
        
    def add_rectangle(self, rect: Rectangle) -> None:
        self.rectangles.append(rect)
        self.update_treeview()
        
    def update_treeview(self) -> None:
        for element in self.treeview.get_children():
            self.treeview.delete(element)

        for rect in self.rectangles:
            self.treeview.insert("", "end", values=(rect.index, rect.width, rect.height))