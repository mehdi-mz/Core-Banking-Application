from ttkbootstrap import Frame , Label , Entry , Button
from ttkbootstrap.style import SUCCESS,DANGER
from Presentation.Components.password_component import PasswordComponent
from Presentation.Components.captcha_component import Captchacomponent
from BusinessLogic.employee_business_logic import EmployeeBusinessLogic
from Common.Decorators.performance_logger_decorator import PerformanceLogger
from  Common.entities.Enums.employee_role import EmployeeRole

class LoginFrame(Frame):
    def __init__(self,window,manager,employee_business:EmployeeBusinessLogic):
        super().__init__(window)
        self.manager=manager
        self.employee_business = employee_business

        self.columnconfigure(1,weight=1)


        self.header_label=Label(self,text="-------------- Login Forme --------------")
        self.header_label.grid(row=0,columnspan=2,column=0,pady=(5,20))

        self.username_label=Label(self,text="Username")
        self.username_label.grid(row=1,column=0,pady=(0,10),padx=10,sticky="e")
        self.username_entry=Entry(self)
        self.username_entry.grid(row=1,column=1,padx=(0,10),pady=(0,10),sticky="ew")

        self.password_label = Label(self,text="Password")
        self.password_label.grid(row=2,column=0, pady=(0, 10), padx=10, sticky="e")
        self.password_component = PasswordComponent(self)
        self.password_component.grid(row=2,column=1, padx=(0, 10), pady=(0, 10),sticky="ew")

        self.erorr_label = Label(self)
        self.erorr_label.grid(row=3, column=1, pady=(0, 10), padx=10)

        self.captcha_component=Captchacomponent(self)
        self.captcha_component.grid(row=4,column=1,padx=10,pady=(0,10),sticky="ew")

        # self.remember_me_checkbutten=Checkbutton(self,text="Remember Me")
        # self.remember_me_checkbutten.grid(row=5,column=1,pady=(0,10),sticky="w")

        self.butten_login=Button(self,text="Login",command=self.butten_login_clicked,bootstyle=SUCCESS)
        self.butten_login.grid(row=6,columnspan=2,column=0,pady=(0,10),padx=10,sticky="ew")

        self.butten_register = Button(self, text="Register",command=self.butten_register_clicked)
        self.butten_register.grid(row=7,columnspan=2, column=0, pady=(0, 10), padx=10, sticky="ew")


    def butten_register_clicked(self):
        self.manager.show_frame("Register")




    @PerformanceLogger
    def butten_login_clicked(self):

        entry_data_captcha=self.captcha_component.get_entry_data()
        data_captcha=self.captcha_component.get_data_captcha()
        username=self.username_entry.get()
        password=self.password_component.get_password_value()
        response = self.employee_business.login(username,password,entry_data_captcha,data_captcha)
        self.erorr_label.config(text="")

        if response.success:
            employee = self.manager.current_user=response.data
            if employee.role_id ==EmployeeRole.Admin:
                home_frame=self.manager.show_frame("home admin")
                home_frame.set_current_user(response.data)
                self.username_entry.delete(0,"end")
                self.password_component.clear()
                self.captcha_component.clear_captcha()
            else:
                home_frame = self.manager.show_frame("Home")
                home_frame.set_current_user(response.data)
                self.username_entry.delete(0, "end")
                self.password_component.clear()
                self.captcha_component.clear_captcha()
        else:
            self.erorr_label.config(text=response.message,bootstyle=DANGER)
            self.captcha_component.butten_refresh_clicked()
