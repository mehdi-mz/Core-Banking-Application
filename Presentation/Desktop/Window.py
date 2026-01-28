# from tkinter import Tk
from ttkbootstrap import Window

class ApplicationWindow(Window):
    def __init__(self):
        super().__init__(themename="darkly")

        self.rowconfigure(1,weight=1)
        self.columnconfigure(0,weight=1)

        self.title("Core Banking Application")


    def resaiz(self,width,height):
        self.update_idletasks()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        y-=100
        x-=80
        self.geometry(f"{width}x{height}+{x}+{y}")

    def show(self):
        self.mainloop()

        