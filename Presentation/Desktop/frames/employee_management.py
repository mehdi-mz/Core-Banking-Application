from ttkbootstrap import Frame,Label,Entry,Button,PhotoImage,Treeview
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.style import LIGHT,INFO
from Common.Decorators.performance_logger_decorator import PerformanceLogger



class EmployeeManagmentFrame(Frame):
    def __init__(self,window,manager,employee_bisiness):
        super().__init__(window)

        self.employee_bisiness = employee_bisiness
        self.manager=manager


        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(3,weight=1)

        self.header_label = Label(self, text="------------ Employee Manager Form ------------")
        self.header_label.grid(row=0, column=0, columnspan=5, pady=10, padx=10)

        self.arrow_image=PhotoImage(file=r"assets\image\icons8-arrow-30.png").subsample(2,2)
        self.arrow_butten=Button(self,image=self.arrow_image,command=self.arrow_butten_clicked,bootstyle=LIGHT)
        self.arrow_butten.grid(row=0,column=0,padx=(5,10),pady=10,sticky="w")

        self.search_entry = Entry(self)
        self.search_entry.grid(row=1, column=0, columnspan=4, pady=(0, 10), padx=10, sticky="ew")
        self.search_entry.bind("<KeyRelease>", self.on_search_live)

        self.search_button = Button(self, text="Search",command=self.search_clicked)
        self.search_button.grid(row=1, column=4, pady=(0, 10), padx=(0, 10), sticky="w")

        self.create_employee_button = Button(self, text="Create Employee",bootstyle=INFO,command=self.create_employee_clicked)
        self.create_employee_button.grid(row=2, column=0, pady=(0, 10), padx=10, sticky="ew")


        self.deactivated_employee_button = Button(self, text="Deactivated Employees",bootstyle=INFO
                                                  ,command=self.deactivated_employees_button_clicked)
        self.deactivated_employee_button.grid(row=2, column=1, pady=(0, 10), padx=(0, 10), sticky="ew")

        self.request_button = Button(self, text="Request",bootstyle=INFO,command=self.request_button_clicked)
        self.request_button.grid(row=2, column=2, pady=(0, 10), padx=(0, 10), sticky="ew")

        self.update_employee_button = Button(self, text="Update Employee",state="disabled",bootstyle=INFO
                                             ,command=self.update_employee_clicked)
        self.update_employee_button.grid(row=2, column=3, pady=(0, 10), padx=(0, 10), sticky="ew")

        self.refresh = PhotoImage(file=r"assets\image\icons8-refresh-50-2.png").subsample(3, 3)
        self.refresh_butten = Button(self, image=self.refresh, command=self.refresh_butten_clicked, bootstyle=LIGHT)
        self.refresh_butten.grid(row=2, column=4, padx=(5, 10), pady=(10, 20), sticky="e")

        self.employee_list_treeview=Treeview(self,columns=(  "firstname_owner",
                                                            "lastname_owner",
                                                            "national_code",
                                                            "username",
                                                            "status",
                                                             "accept_date"))

        self.employee_list_treeview.heading("#0", text="#")
        self.employee_list_treeview.heading("#1", text="First Name")
        self.employee_list_treeview.heading("#2", text="Last Name")
        self.employee_list_treeview.heading("#3", text="National Code")
        self.employee_list_treeview.heading("#4", text="User Name")
        self.employee_list_treeview.heading("#5", text="Status")
        self.employee_list_treeview.heading("#6", text="Accept Date")


        self.employee_list_treeview.column("#0",width=50,stretch=False)

        for col in self.employee_list_treeview["columns"]:
            self.employee_list_treeview.column(col, width=120, anchor="center")



        self.employee_list_treeview.grid(row=3,column=0,columnspan=5,pady=(0,10),padx=10,sticky="ewsn")

        self. employee_list_treeview.bind("<<TreeviewSelect>>",self.employee_select)

        pagination_frame = Frame(self)
        pagination_frame.grid(row=4, column=0, columnspan=5, pady=(0, 10))

        self.previous_page_butten = Button(pagination_frame, text="<", command=self.load_previous_data_to_treeview,
                                           bootstyle=INFO)
        self.previous_page_butten.grid(row=0, column=0, padx=20)

        self.current_page_label = Label(pagination_frame, text="1")
        self.current_page_label.grid(row=0, column=1, padx=20)

        self.next_page_butten = Button(pagination_frame, text=">", command=self.load_next_data_to_treeview,
                                       bootstyle=INFO)
        self.next_page_butten.grid(row=0, column=2, padx=20)

    def update_employee_clicked(self):
        self.employee_id = self.employee_list_treeview.selection()[0]
        update_employee = self.manager.show_frame("update employee")
        update_employee.set_entry(self.employee_id)



    def employee_select(self,event):
        selection = self.employee_list_treeview.selection()
        if selection:
            self.update_employee_button.config(state="normal")
        else:
            self.update_employee_button.config(state="disabled")


    def arrow_butten_clicked(self):
        self.search_entry.delete(0,"end")
        self.manager.back()

    def refresh_butten_clicked(self):
        self.load_data_to_employee_management_treeview()



    @PerformanceLogger
    def load_data_to_employee_management_treeview(self,page_number=1,page_size=15):
        if page_number == 1 :
            self.current_page_label.config(text="1")
            self.next_page_butten.config(state="normal")
        self.page_size =page_size
        term = self.search_entry.get().strip()
        response = self.employee_bisiness.employee_management(page_number,page_size, term if term else None)



        if response.success:
            for row in self.employee_list_treeview.get_children():
                self.employee_list_treeview.delete(row)



            for index,employee in enumerate(response.data):
                rownumber = (page_number - 1) * page_size + index + 1
                self.employee_list_treeview.insert(
                    "",
                    "end",
                    iid=employee.id,
                    text=str(rownumber),
                    values=(
                        employee.firstname,
                        employee.lastname,
                        employee.national_code,
                        employee.username,
                        employee.status_id.name,
                        employee.accept_date
                    )
                )
            return response.data
        else:
            Messagebox.show_error(response.message,"Failed!")


    def load_next_data_to_treeview(self):
        current_size=int(self.current_page_label.cget("text"))
        next_page=current_size+1
        data = self.load_data_to_employee_management_treeview(next_page)
        self.current_page_label.config(text=str(next_page))
        if not data or len(data) < self.page_size:
                self.next_page_butten.config(state="disabled")

    def load_previous_data_to_treeview(self):
        current_size=int(self.current_page_label.cget("text"))
        previous_page=max(1,current_size-1)
        self.load_data_to_employee_management_treeview(previous_page)
        self.current_page_label.config(text=str(previous_page))
        self.next_page_butten.config(state="normal")

    @PerformanceLogger
    def request_button_clicked(self):

        request_employee= self.manager.show_frame("request employee")
        request_employee.data_load_to_request_treeview()


    def create_employee_clicked(self):
        self.manager.show_frame("Register")

    def deactivated_employees_button_clicked(self):
        deactivated_employee = self.manager.show_frame("deactivated employee")
        deactivated_employee.load_data_to_employee_management_treeview()

    def search_clicked(self):
        self.load_data_to_employee_management_treeview()

    def on_search_live(self,event):
        self.search_clicked()
























