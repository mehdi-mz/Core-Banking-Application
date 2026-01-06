
from ttkbootstrap import Frame,Label,Entry,Button,PhotoImage
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.style import LIGHT,DANGER,SUCCESS,WARNING
from BusinessLogic.employee_business_logic import EmployeeBusinessLogic
from Common.Decorators.performance_logger_decorator import PerformanceLogger
from Common.entities.Enums.employee_role import EmployeeRole
from Common.entities.Enums.employee_status import EmployeeStatus


class EmployeeRequestApprovalFrame(Frame):
    def __init__(self,window,manager,employee_business:EmployeeBusinessLogic):
        super().__init__(window)

        self.manager=manager
        self.employee_business=employee_business

        self.grid_columnconfigure(1,weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)

        self.header_label=Label(self,text="-------- Request Approval Frame --------")
        self.header_label.grid(row=0,columnspan=5,column=0,padx=10,pady=10)



        self.image_arrow = PhotoImage(file=r"assets\image\icons8-arrow-30.png").subsample(2, 2)
        self.butten_arrow = Button(self, image=self.image_arrow, command=self.butten_arrow_clicked,bootstyle=LIGHT)
        self.butten_arrow.grid(row=0, column=0, padx=10 ,pady=(5, 20), sticky="w")

        self.accept_button = Button(self, text="Accept Employee ✔", bootstyle=SUCCESS,command=self.accept_employee)
        self.accept_button.grid(row=1, column=4, padx=10, pady=(10,25), sticky="w")

        self.reject_button = Button(self, text=" Reject Employee ❌", bootstyle=DANGER,command=self.reject_employee)
        self.reject_button.grid(row=1, column=3, padx=10, pady=(10,25), sticky="e")

        self.label_firstname=Label(self,text="First Name")
        self.label_firstname.grid(row=2,column=0,padx=10,pady=(0,10),sticky="e")
        self.entry_firstname=Entry(self)
        self.entry_firstname.grid(row=2,column=1,pady=(0,10),padx=(0,10),sticky="ew")

        self.label_lastname = Label(self, text="Last Name")
        self.label_lastname.grid(row=2, column=3, padx=10, pady=(0, 10), sticky="e")
        self.entry_lastname = Entry(self)
        self.entry_lastname.grid(row=2, column=4, pady=(0, 10), padx=(0, 10), sticky="ew")

        self.label_username = Label(self, text="Username")
        self.label_username.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="e")
        self.entry_username = Entry(self)
        self.entry_username.grid(row=3, column=1,columnspan=4, pady=(0, 10), padx=(0, 10), sticky="ew")

        self.label_nationalcode = Label(self, text="National Code")
        self.label_nationalcode.grid(row=4, column=0, padx=10, pady=(0, 10), sticky="e")
        self.entry_nationalcode = Entry(self)
        self.entry_nationalcode.grid(row=4, column=1,columnspan=4, pady=(0, 10), padx=(0, 10), sticky="ew")

        self.label_email = Label(self, text="Email")
        self.label_email.grid(row=5, column=0, padx=10, pady=(0, 10), sticky="e")
        self.entry_email = Entry(self)
        self.entry_email.grid(row=5, column=1,columnspan=4, pady=(0, 10), padx=(0, 10), sticky="ew")

        self.label_status = Label(self, text="Employee Status")
        self.label_status.grid(row=6, column=0, padx=10, pady=(0, 10), sticky="e")
        self.entry_status = Entry(self,state="readonly")
        self.entry_status.grid(row=6, column=1,columnspan=4, pady=(0, 10), padx=(0, 10), sticky="ew")

        self.label_employeerole = Label(self, text="Employee Role")
        self.label_employeerole.grid(row=7, column=0, padx=10, pady=(0, 10), sticky="e")
        self.entry_employeerole = Entry(self,state="readonly")
        self.entry_employeerole.grid(row=7, column=1,columnspan=4, padx=(0, 10), sticky="ew")

        self.error_label=Label(self)
        self.error_label.grid(row=8,column=0,columnspan=5,pady=10)


        self.butten_save=Button(self,text="Save ✔",command=self.save_adit_employee_request,bootstyle=SUCCESS)
        self.butten_save.grid(row=9,column=0,columnspan=5,pady=(5,10))

    @PerformanceLogger
    def save_adit_employee_request(self):
        new_firstname=self.entry_firstname.get()
        new_lastname=self.entry_lastname.get()
        new_username=self.entry_username.get()
        new_nationalcode=self.entry_nationalcode.get()
        new_email=self.entry_email.get()
        update_employee = self.employee_business.update_profile(self.employee_id,new_firstname,new_lastname,
                                                                new_username,new_nationalcode,new_email,None,None)
        if update_employee.success:
            Messagebox.show_info(update_employee.message,"Success")
            self.error_label.config(text="")
        else:
            self.error_label.config(text=update_employee.message,bootstyle=DANGER)



    def butten_arrow_clicked(self):
            self.manager.back()
            self.error_label.config(text="")

    @PerformanceLogger
    def set_entry_employee_request(self,employee_id):
        self.employee_id = employee_id
        self.entry_firstname.delete(0, "end")
        self.entry_lastname.delete(0, "end")
        self.entry_username.delete(0, "end")
        self.entry_nationalcode.delete(0, "end")
        self.entry_email.delete(0, "end")

        response = self.employee_business.get_employee_by_id(employee_id)
        if response.success:
            employee = response.data
            self.entry_firstname.insert(0,employee.firstname)
            self.entry_lastname.insert(0, employee.lastname)
            self.entry_username.insert(0, employee.username)
            self.entry_nationalcode.insert(0, employee.national_code)
            self.entry_email.insert(0, employee.email)

            self.entry_status.config(state="normal")
            self.entry_status.delete(0, "end")
            if employee.status_id == EmployeeStatus.Pending:
                self.entry_status.insert(0,"Pending")
                self.entry_status.config(bootstyle=WARNING)
                self.reject_button.config(state="normal")
            elif employee.status_id == EmployeeStatus.Rejected:
                self.entry_status.insert(0, "Rejected")
                self.entry_status.config(bootstyle=DANGER)
                self.reject_button.config(state="disabled")
            self.entry_status.config(state="readonly")

            self.entry_employeerole.config(state="normal")
            self.entry_employeerole.delete(0, "end")
            if employee.role_id == EmployeeRole.Admin:
                self.entry_employeerole.insert(0,"Admin")
            elif employee.role_id == EmployeeRole.Banker:
                self.entry_employeerole.insert(0, "Banker")
            self.entry_employeerole.config(state="readonly")

    def accept_employee(self):
        response = self.employee_business.accept_employee(self.employee_id)
        if response.success:
            Messagebox.show_info(response.message,"success ✅")
            request_employee = self.manager.back()
            request_employee.data_load_to_request_treeview()
        else:
            Messagebox.show_error(response.message,"error ❌")

    def reject_employee(self):
        response = self.employee_business.reject_employee(self.employee_id)
        if response.success:
            Messagebox.show_info(response.message, "success ✅")
            request_employee = self.manager.back()
            request_employee.data_load_to_request_treeview()
        else:
            Messagebox.show_error(response.message, "error ❌")
