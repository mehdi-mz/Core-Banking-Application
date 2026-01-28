
from ttkbootstrap import Frame,Entry,Button,PhotoImage
from ttkbootstrap.style import INFO
class PasswordComponent(Frame):
    def __init__(self,master):
        super().__init__(master)

        self.columnconfigure(0,weight=1)



        self.eye_closed = PhotoImage(
            file=r"assets\image\icons8-closed-eye-50.png").subsample(3, 3)
        self.eye_open = PhotoImage(
            file=r"assets\image\icons8-eye-50.png").subsample(3, 3)

        self.entry_password = Entry(self, show="*")
        self.entry_password.grid(row=0, column=0, sticky="ew")

        self.butten_show = Button(self, image=self.eye_open, command=self.change_status, bootstyle=INFO)
        self.butten_show.grid(row=0, column=1, sticky="ew")

        self.current_state = False
    def change_status(self):
        if self.current_state:
            self.entry_password.config(show="*")
            self.butten_show.config(image=self.eye_open)
            self.current_state = False
        else:
            self.entry_password.config(show="")
            self.butten_show.config(image=self.eye_closed)
            self.current_state = True

    def get_password_value(self):
        password_value=self.entry_password.get()
        return password_value


    def clear(self):
        self.entry_password.delete(0,"end")