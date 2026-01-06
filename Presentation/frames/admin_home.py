from ttkbootstrap import Frame,Label,Button
from Common.entities.employee import Employee
from Common.Decorators.performance_logger_decorator import PerformanceLogger




class AdminHomeFrame(Frame):
    def __init__(self,window,manager):
        super().__init__(window)
        self.manager=manager
        # self.navbar = navbar


        self.grid_columnconfigure(0,weight=1)

        self.header_label= Label(self)
        self.header_label.grid(row=0,column=0,columnspan=2,pady=10)

        self.my_profile_butten= Button(self,text="My Profile",command=self.my_profile_clicked)
        self.my_profile_butten.grid(row=1,column=0,columnspan=2,pady=(0,10),padx=10,sticky="ew")

        self.account_management_butten = Button(self, text="Account Management",command=self.account_management_clicked)
        self.account_management_butten.grid(row=2, column=0, columnspan=2, pady=(0, 10), padx=10,sticky="ew")

        self.employee_management_butten = Button(self, text="Employee Management",command=self.employee_management_clicked)
        self.employee_management_butten.grid(row=3, column=0, columnspan=2, pady=(0, 10), padx=10, sticky="ew")

        self.logout_butten = Button(self, text="Logout",command=self.logout_clicked)
        self.logout_butten.grid(row=4, column=0, columnspan=2, pady=(0, 10), padx=10,sticky="ew")


    @PerformanceLogger
    def account_management_clicked(self):
        account_manajment= self.manager.show_frame("account manajment")
        account_manajment.load_data_to_account_management_treeview()

    def employee_management_clicked(self):
        employee_management=self.manager.show_frame("employee management")
        employee_management.load_data_to_employee_management_treeview()

    def set_current_user(self,current_user:Employee):
        self.header_label.config(text=f"------- Welcom {current_user.full_name()} -------")
        self.current_user = current_user




    def logout_clicked(self):
        self.manager.show_frame("Login")

    def my_profile_clicked(self):
        my_profile = self.manager.show_frame("My Profile")
        my_profile.set_entry()
