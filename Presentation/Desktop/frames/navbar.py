from tkinter import BooleanVar
from ttkbootstrap import Frame,Checkbutton




class Navbar(Frame):
    def __init__(self,window,manager):
        super().__init__(window)


        self.manager = manager

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)

        self.theme_var = BooleanVar(value=True)
        self.theme_checkbutton = Checkbutton(self,bootstyle="light-round-toggle",variable=self.theme_var
                                            ,text="Dark Mode",command=self.theme_checkbutton_clicked)
        self.theme_checkbutton.grid(row=0,column=2,padx=10,pady=10,sticky="e")



    def theme_checkbutton_clicked(self):

        if self.theme_var.get():
            self.manager.window.style.theme_use("darkly")
        else:
            self.manager.window.style.theme_use("flatly")
