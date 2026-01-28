
from ttkbootstrap import Frame,Button,Label,PhotoImage
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.style import LIGHT,DANGER

from Presentation.Desktop.Components.password_component import PasswordComponent
from BusinessLogic.employee_business_logic import EmployeeBusinessLogic
from Common.Decorators.performance_logger_decorator import PerformanceLogger


class AdminResetEmployeePasswordFrame(Frame):
    def __init__(self,window,manager,employee_business:EmployeeBusinessLogic):
        super().__init__(window)
        self.manager=manager
        self.employee_business = employee_business

        self.grid_columnconfigure(1,weight=1)


        self.header_label=Label(self,text="------------- Change Password -------------")
        self.header_label.grid(row=0,column=0,columnspan=3,pady=10)

        self.arrow_image = PhotoImage(file=r"assets\image\icons8-arrow-30.png").subsample(2, 2)
        self.arrow_butten = Button(self, image=self.arrow_image, command=self.arrow_butten_clicked, bootstyle=LIGHT)
        self.arrow_butten.grid(row=0, column=0, padx=(5, 10), pady=10, sticky="w")


        self.label_new_password=Label(self,text="New Password")
        self.label_new_password.grid(row=1,column=0,pady=(0,10),padx=10,sticky="e")
        self.password_component=PasswordComponent(self)
        self.password_component.grid(row=1,column=1,columnspan=2,pady=(0,10),padx=(0,10),sticky="ew")

        self.label_confirm_password = Label(self, text="Confirm Password")
        self.label_confirm_password.grid(row=2, column=0, pady=(0, 10), padx=10, sticky="e")
        self.confirm_password_component =PasswordComponent(self)
        self.confirm_password_component.grid(row=2, column=1, columnspan=2, pady=(0, 10), padx=(0, 10), sticky="ew")

        self.error_label=Label(self)
        self.error_label.grid(row=3,column=0,columnspan=3,pady=(0,10))


        self.butten_update_password=Button(self,text="Update Password",command=self.butten_update_password_clicked)
        self.butten_update_password.grid(row=4,column=0,columnspan=3,pady=(0,10))


    def arrow_butten_clicked(self):
        self.manager.back()

    @PerformanceLogger
    def butten_update_password_clicked(self):

        new_password = self.password_component.get_password_value()
        confirm_password = self.confirm_password_component.get_password_value()
        response = self.employee_business.reset_password(self.employee_id,new_password,confirm_password,None,None)


        if response.success:
            Messagebox.show_info(response.message,"Success ✅")
            self.password_component.clear()
            self.confirm_password_component.clear()
            self.error_label.config(text="")
            self.manager.back()
        else:
            self.error_label.config(text=response.message,bootstyle=DANGER)

    def set_employee_id(self,employee_id):
        self.employee_id = employee_id










