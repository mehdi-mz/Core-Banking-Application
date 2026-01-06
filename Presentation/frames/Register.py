from ttkbootstrap import Frame,Label,Entry,Button,PhotoImage
from ttkbootstrap.style import LIGHT,DANGER
from ttkbootstrap.dialogs import Messagebox
from Common.Decorators.performance_logger_decorator import PerformanceLogger
from Presentation.Components.password_component import PasswordComponent


class RegisterFrame(Frame):
    def __init__(self,window,manager,employee_business):
        super().__init__(window)
        self.manager = manager
        self.employee_business =employee_business



        self.columnconfigure(1,weight=1)

        self.header_label=Label(self,text="------ Register Forme ------")
        self.header_label.grid(row=0,columnspan=2,column=0,pady=(5,20))

        self.label_firstname=Label(self,text="First Name")
        self.label_firstname.grid(row=1,column=0,padx=10,pady=(0,10),sticky="w")
        self.entry_firstname=Entry(self)
        self.entry_firstname.grid(row=1,column=1,padx=(0,10),pady=(0,10),sticky="ew")

        self.label_lastname = Label(self, text="Last Name")
        self.label_lastname.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="w")
        self.entry_lastname = Entry(self)
        self.entry_lastname.grid(row=2, column=1, padx=(0, 10), pady=(0, 10), sticky="ew")

        self.label_nationalcode = Label(self, text="National Code")
        self.label_nationalcode.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="w")
        self.entry_nationalcode = Entry(self)
        self.entry_nationalcode.grid(row=3, column=1, padx=(0, 10), pady=(0, 10), sticky="ew")

        self.label_email = Label(self, text="Email")
        self.label_email.grid(row=4, column=0, padx=10, pady=(0, 10), sticky="w")
        self.entry_email = Entry(self)
        self.entry_email.grid(row=4, column=1, padx=(0, 10), pady=(0, 10), sticky="ew")

        self.label_username = Label(self, text="User Name")
        self.label_username.grid(row=5, column=0, padx=10, pady=(0, 10), sticky="w")
        self.entry_username = Entry(self)
        self.entry_username.grid(row=5, column=1, padx=(0, 10), pady=(0, 10), sticky="ew")

        self.label_password = Label(self, text="Password")
        self.label_password.grid(row=6, column=0, padx=10, pady=(0, 10), sticky="w")
        self.entry_password = PasswordComponent(self)
        self.entry_password.grid(row=6, column=1, padx=(0, 10), pady=(0, 10), sticky="ew")

        self.label_confirm_password = Label(self, text="Confirm Password")
        self.label_confirm_password.grid(row=7, column=0, padx=10, pady=(0, 10), sticky="w")
        self.entry_confirm_password =PasswordComponent(self)
        self.entry_confirm_password.grid(row=7, column=1, padx=(0, 10), pady=(0, 10), sticky="ew")

        self.error_label = Label(self)
        self.error_label.grid(row=8,column=0,columnspan=2,padx=10,pady=10)

        self.butten_register=Button(self,text="Register Now",command=self.butten_register_clicked)
        self.butten_register.grid(row=9,column=0,columnspan=2,padx=10,pady=(0,10),sticky="ew")

        self.image_arrow=PhotoImage(file=r"assets\image\icons8-arrow-30.png").subsample(2,2)
        self.butten_arrow=Button(self,image=self.image_arrow,command=self.butten_arrow_clicked,bootstyle=LIGHT)
        self.butten_arrow.grid(row=0,column=0,padx=10,pady=(5,20),sticky="w")



    def butten_arrow_clicked(self):
        self.error_label.config(text="")
        self.manager.back()

    @PerformanceLogger
    def butten_register_clicked(self):
        firstname=self.entry_firstname.get()
        lastname=self.entry_lastname.get()
        nationalcode=self.entry_nationalcode.get()
        email=self.entry_email.get()
        username=self.entry_username.get()
        password=self.entry_password.get_password_value()
        confirm_password = self.entry_confirm_password.get_password_value()

        response = self.employee_business.register_employee(firstname, lastname, nationalcode,
                                                            email, username,password ,confirm_password)
        if response.success:
            Messagebox.show_info(response.message,"✅")
            self.error_label.config(text="")

            self.entry_firstname.delete(0,"end")
            self.entry_lastname.delete(0,"end")
            self.entry_nationalcode.delete(0,"end")
            self.entry_email.delete(0,"end")
            self.entry_username.delete(0,"end")
            self.entry_password.clear()
            self.entry_confirm_password.clear()

        else:
            self.error_label.config(text=response.message,bootstyle=DANGER)
