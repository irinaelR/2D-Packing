from tkinter import * # type: ignore
from tkinter import ttk
from tkinter import messagebox

from objet.rectangle import Rectangle

class Formulaire(Frame):
    
    def __init__(self, master, conteneur, conteneur_list, treeview_list, choose_fit, define_conteneur, define_rect, **kwargs) -> None:
        super().__init__(master, **kwargs) 
        
        self.rect_indice = 1
        
        self.conteneur = conteneur
        self.conteneur_list = conteneur_list
        self.treeview_list = treeview_list
        self.choose_fit = choose_fit
        self.define_conteneur = define_conteneur
        self.define_rect = define_rect
        
        self._bac_info = LabelFrame(self, text="Information bac")
        self._bac_width = Label(self._bac_info, text="Width")
        self._bac_width_entry = Entry(self._bac_info, foreground='gray')
        self._bac_height = Label(self._bac_info, text="height")
        self._bac_height_entry = Entry(self._bac_info, foreground='gray')
        self._bac_button = Button(self._bac_info, text="Valider", command=self.validate_and_create_canvas)
        
        self._rect_info = LabelFrame(self, text="Information rectangle")
        self._rect_width = Label(self._rect_info, text="Width")
        self._rect_width_entry = Entry(self._rect_info)
        self._rect_height = Label(self._rect_info, text="height")
        self._rect_height_entry = Entry(self._rect_info)
        self._rect_button = Button(self._rect_info, text="Valider", command = self.validate_and_append_treeview)
        
        self._type_fit = LabelFrame(self, text="Fit type")
        self._combobox_value = StringVar()
        self._type_label = Label(self._type_fit, text="Choisissez le type de fit (jsp xD)")
        self._type_combobox = ttk.Combobox(self._type_fit, textvariable=self._combobox_value, state='readonly')
        
        
    def _get_bac_info(self) -> LabelFrame:
        return self._bac_info 
    
    def _set_bac_info(self, bac_info: LabelFrame) -> None:
        self._bac_info = bac_info   
        
    def _get_rect_info(self) -> LabelFrame:
        return self._rect_info 
    
    def _set_rect_info(self, rect_info: LabelFrame) -> None:
        self._rect_info = rect_info   
        
    def _get_type_fit(self) -> LabelFrame:
        return self._type_fit 
    
    def _set_type_fit(self, type_fit: LabelFrame) -> None:
        self._type_fit = type_fit   
        
    bac_info: LabelFrame = property(_get_bac_info, _set_bac_info)
    rect_info: LabelFrame = property(_get_rect_info, _set_rect_info)
    type_fit: LabelFrame = property(_get_type_fit, _set_type_fit)
    
    def width_click(self, event):
        if self._bac_width_entry.get() == "Max width: 900px":
            self._bac_width_entry.delete(0, END)
            self._bac_width_entry.configure(foreground="black")

    def width_out(self, event):
        if self._bac_width_entry.get() == "":
            self._bac_width_entry.insert(0, "Max width: 900px")
            self._bac_width_entry.configure(foreground="gray")
    
    def height_click(self, event):
        if self._bac_height_entry.get() == "Max height: 550px":
            self._bac_height_entry.delete(0, END)
            self._bac_height_entry.configure(foreground="black")

    def height_out(self, event):
        if self._bac_height_entry.get() == "":
            self._bac_height_entry.insert(0, "Max height: 550px")
            self._bac_height_entry.configure(foreground="gray")
        
    def initialize(self) -> None:
        self.bac_info.grid(row=0, column=0, padx=20, pady=2)
        self._bac_width.grid(row=0, column=0, pady=(3, 0))
        self._bac_width_entry.grid(row=1, column=0, padx=10, pady=(0, 2))
        self._bac_width_entry.insert(0, "Max width: 900px")
        self._bac_height.grid(row=0, column=1, pady=(3, 0))
        self._bac_height_entry.grid(row=1, column=1, padx=10, pady=(0, 2))
        self._bac_height_entry.insert(0, "Max height: 550px")
        self._bac_button.grid(row=2, column=0, columnspan=2, pady=(0, 3))
        # width
        self._bac_width_entry.bind("<FocusIn>", self.width_click)
        self._bac_width_entry.bind("<FocusOut>", self.width_out)
        #height
        self._bac_height_entry.bind("<FocusIn>", self.height_click)
        self._bac_height_entry.bind("<FocusOut>", self.height_out)
        
        self.rect_info.grid(row=0, column=1, padx=20, pady=2)
        self._rect_width.grid(row=0, column=0, pady=(3, 0))
        self._rect_width_entry.grid(row=1, column=0, padx=10, pady=(0, 2))
        self._rect_height.grid(row=0, column=1, pady=(3, 0))
        self._rect_height_entry.grid(row=1, column=1, padx=10, pady=(0, 2))
        self._rect_button.grid(row=2, column=0, columnspan=2, pady=(0, 3))
        
        self.type_fit.grid(row=0, column=2, padx=20, pady=2)
        self._type_label.grid(row=0, columnspan=2, padx=10, pady=(0, 5))
        self._type_combobox['values'] = ('First fit decreasing height (FFDH)',
                                         'Next fit decreasing height (NFDH)',
                                         'Best fit',
                                         'Brute force',   
                                         'Brute force avec rotation'   
                                        )
        self._type_combobox.grid(row=1, columnspan=2, pady=(0, 10))
        self._type_combobox.bind('<<ComboboxSelected>>', self.modify_fit)

    def validate_and_create_canvas(self) -> None:
            try:
                width = int(self._bac_width_entry.get())
                height = int(self._bac_height_entry.get())

                if width <= 0 or height <= 0:
                    raise ValueError("Dimensions must be positive integers")
                elif width > 900 or height > 550:
                    raise ValueError("Higher than max")

                self.conteneur(width, height)
                self.define_conteneur(width, height)

            except ValueError as e:
                messagebox.showerror("Invalid input", "Please enter valid integers for width and height")

    def validate_and_append_treeview(self) -> None:
            try:
                width = int(self._rect_width_entry.get())
                height = int(self._rect_height_entry.get())

                if width <= 0 or height <= 0:
                    raise ValueError("Dimensions must be positive integers")

                self.conteneur_list(Rectangle(self.rect_indice, width, height))
                self.treeview_list(Rectangle(self.rect_indice, width, height))

                self.rect_indice += 1

            except ValueError as e:
                messagebox.showerror("Invalid input", "Please enter valid integers for width and height")
                
    def modify_fit(self, event) -> None:
        try:
            width = int(self._bac_width_entry.get())
            height = int(self._bac_height_entry.get())

            if width <= 0 or height <= 0:
                raise ValueError("Dimensions must be positive integers")

            rect_temp: list[Rectangle] = []
            rect_fitted_temp: list[Rectangle] = []
            print(self._combobox_value.get())
            self.choose_fit(self._combobox_value.get(), rect_temp, rect_fitted_temp)
            self.define_rect(rect_temp, rect_fitted_temp)

        except ValueError as e:
            messagebox.showerror("Invalid input", "Please insert container")
        