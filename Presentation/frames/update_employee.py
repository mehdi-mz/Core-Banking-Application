from ttkbootstrap import Frame,Label,Entry,Button,PhotoImage,Combobox
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.style import LIGHT,DANGER,SUCCESS,INFO
from BusinessLogic.employee_business_logic import EmployeeBusinessLogic
from Common.Decorators.performance_logger_decorator import PerformanceLogger
from Common.entities.Enums.employee_role import EmployeeRole
from Common.entities.Enums.employee_status import EmployeeStatus


class UpdateEmployeeFrame(Frame):
    def __init__(self,window,manager,employee_business:EmployeeBusinessLogic):
        super().__init__(window)

        self.manager=manager
        self.employee_business=employee_business

        self.grid_columnconfigure(1,weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)

        self.header_label=Label(self,text="----------- Update Employee -----------")
        self.header_label.grid(row=0,columnspan=5,column=0,padx=10,pady=10)

        self.image_arrow = PhotoImage(file=r"assets\image\icons8-arrow-30.png").subsample(2, 2)
        self.butten_arrow = Button(self, image=self.image_arrow, command=self.butten_arrow_clicked, bootstyle=LIGHT)
        self.butten_arrow.grid(row=0, column=0, padx=10, pady=(5, 20), sticky="w")

        self.label_firstname=Label(self,text="First Name")
        self.label_firstname.grid(row=1,column=0,padx=10,pady=(0,10),sticky="e")
        self.entry_firstname=Entry(self)
        self.entry_firstname.grid(row=1,column=1,pady=(0,10),padx=(0,10),sticky="ew")

        self.label_lastname = Label(self, text="Last Name")
        self.label_lastname.grid(row=1, column=3, padx=10, pady=(0, 10), sticky="e")
        self.entry_lastname = Entry(self)
        self.entry_lastname.grid(row=1, column=4, pady=(0, 10), padx=(0, 10), sticky="ew")

        self.label_username = Label(self, text="Username")
        self.label_username.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="e")
        self.entry_username = Entry(self)
        self.entry_username.grid(row=2, column=1,columnspan=4, pady=(0, 10), padx=(0, 10), sticky="ew")

        self.label_nationalcode = Label(self, text="National Code")
        self.label_nationalcode.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="e")
        self.entry_nationalcode = Entry(self)
        self.entry_nationalcode.grid(row=3, column=1,columnspan=4, pady=(0, 10), padx=(0, 10), sticky="ew")

        self.label_email = Label(self, text="Email")
        self.label_email.grid(row=4, column=0, padx=10, pady=(0, 10), sticky="e")
        self.entry_email = Entry(self)
        self.entry_email.grid(row=4, column=1,columnspan=4, pady=(0, 10), padx=(0, 10), sticky="ew")

        self.label_status = Label(self, text="Employee Status")
        self.label_status.grid(row=5, column=0, padx=10, pady=(0, 10), sticky="e")
        self.entry_status = Combobox(self,values=["Active","Deactive"],state="readonly")
        self.entry_status.grid(row=5, column=1,columnspan=4, pady=(0, 10), padx=(0, 10), sticky="ew")

        self.label_employeerole = Label(self, text="Employee Role")
        self.label_employeerole.grid(row=6, column=0, padx=10, pady=(0, 10), sticky="e")
        self.entry_employeerole = Entry(self,state="readonly")
        self.entry_employeerole.grid(row=6, column=1,columnspan=4, padx=(0, 10), sticky="ew")

        self.error_label=Label(self)
        self.error_label.grid(row=7,column=0,columnspan=5,pady=10)


        self.butten_reset_password=Button(self,text="Reset Password.",bootstyle=INFO,command=self.butten_reset_password_clicked)
        self.butten_reset_password.grid(row=7, column=4, pady=10, padx=(10,20), sticky="e")

        self.butten_save=Button(self,text="Save ✔",command=self.save_update_employee_button_clicked,bootstyle=SUCCESS)
        self.butten_save.grid(row=8,column=0,columnspan=5,pady=(5,10))

    @PerformanceLogger
    def save_update_employee_button_clicked(self):
        new_firstname=self.entry_firstname.get()
        new_lastname=self.entry_lastname.get()
        new_username=self.entry_username.get()
        new_nationalcode=self.entry_nationalcode.get()
        new_email=self.entry_email.get()
        new_status = self.entry_status.get()
        update_employee = self.employee_business.update_profile(self.employee_id,new_firstname,new_lastname,new_username
                                                                ,new_nationalcode,new_email,new_status)
        if update_employee.success:
            Messagebox.show_info(update_employee.message,"Success")
            self.error_label.config(text="")

        else:
            self.error_label.config(text=update_employee.message,bootstyle=DANGER)

    @PerformanceLogger
    def butten_reset_password_clicked(self):
        admin_reset_password = self.manager.show_frame("admin reset password")
        admin_reset_password.set_employee_id(self.employee_id)


    def butten_arrow_clicked(self):
        self.manager.back()


    @PerformanceLogger
    def set_entry(self,employee_id):
        self.employee_id = employee_id
        response = self.employee_business.get_employee_by_id(employee_id)

        if response.success:
            self.entry_firstname.delete(0,"end")
            self.entry_firstname.insert(0,response.data.firstname)
            self.entry_lastname.delete(0,"end")
            self.entry_lastname.insert(0,response.data.lastname)
            self.entry_username.delete(0,"end")
            self.entry_username.insert(0,response.data.username)
            self.entry_nationalcode.delete(0,"end")
            self.entry_nationalcode.insert(0,response.data.national_code)
            self.entry_email.delete(0,"end")
            self.entry_email.insert(0,response.data.email)
            self.entry_status.config(state="normal")
            self.entry_status.delete(0, "end")
            if response.data.status_id == EmployeeStatus.Active:
                self.entry_status.insert(0,"Active")
                self.entry_status.config(bootstyle=SUCCESS)
            elif response.data.status_id == EmployeeStatus.Deactive:
                self.entry_status.insert(0, "Deactive")
                self.entry_status.config(bootstyle=DANGER)
            self.entry_status.config(state="readonly")
            self.entry_employeerole.config(state="normal")
            self.entry_employeerole.delete(0,"end")
            if response.data.role_id == EmployeeRole.Admin:
                self.entry_employeerole.insert(0,"Admin")
            elif response.data.role_id == EmployeeRole.Banker:
                self.entry_employeerole.insert(0, "Banker")
            self.entry_employeerole.config(state="readonly")
        else:
            Messagebox.show_error("My Profile load failed.","error")


