from ttkbootstrap import Frame,Label,Button,PhotoImage,Treeview,Entry
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.style import LIGHT,INFO
from Common.Decorators.performance_logger_decorator import PerformanceLogger



class RequestEmployeeFrame(Frame):
    def __init__(self,window,manager,employee_business):
        super().__init__(window)


        self.employee_business = employee_business
        self.manager = manager


        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1,weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_rowconfigure(2,weight=1)



        self.grid_rowconfigure(3,weight=1)



        self.header_label = Label(self, text="----------- Request Manager Form -----------")
        self.header_label.grid(row=0, column=0, columnspan=6, pady=10, padx=10)

        self.arrow_image = PhotoImage(file=r"assets\image\icons8-arrow-30.png").subsample(2, 2)
        self.arrow_butten = Button(self, image=self.arrow_image, command=self.arrow_butten_clicked, bootstyle=LIGHT)
        self.arrow_butten.grid(row=0, column=0, padx=(5, 10), pady=10, sticky="w")


        self.search_entry = Entry(self)
        self.search_entry.grid(row=1, column=0, columnspan=5, pady=(0, 10), padx=10, sticky="ew")
        self.search_entry.bind("<KeyRelease>", self.on_search_live)

        self.search_button = Button(self, text="Search",command=self.search_clicked)
        self.search_button.grid(row=1, column=5, pady=(0, 10), padx=(0, 10), sticky="w")

        self.refresh = PhotoImage(file=r"assets\image\icons8-refresh-50-2.png").subsample(3, 3)
        self.refresh_butten = Button(self, image=self.refresh, command=self.refresh_butten_clicked, bootstyle=LIGHT)
        self.refresh_butten.grid(row=1, column=5, padx=(5, 10), pady=(10, 20), sticky="e")

        self.request_treeview=Treeview(self,columns=(
                                                         "first_name",
                                                         "last_name",
                                                         "national_code",
                                                         "username",
                                                         "status",
                                                          "request_date"
                                                         ))
        self.request_treeview.grid(row=2,column=0,columnspan=6,padx=10,sticky="nsew")
        self.request_treeview.column("#0",width=50)
        self.request_treeview.heading("#0",text="#")
        self.request_treeview.heading("#1",text="First Name")
        self.request_treeview.heading("#2",text="Last Name")
        self.request_treeview.heading("#3",text="National Code")
        self.request_treeview.heading("#4",text="User Name")
        self.request_treeview.heading("#5",text="Status")
        self.request_treeview.heading("#6",text="Request Date")

        self.request_treeview.column("#0",width=50,stretch=False)

        for col in self.request_treeview["columns"]:
            self.request_treeview.column(col, width=120, anchor="center")

        self.request_treeview.bind("<Double-1>",self.double_clicked)

        self.reject_butten = Button(self, text="Rejected Employees",command=self.reject_butten_clicked)
        self.reject_butten.grid(row=3,column=5,padx=10,sticky="e")

        pagination_frame = Frame(self)
        pagination_frame.grid(row=3, column=0, columnspan=6)

        self.previous_page_butten = Button(pagination_frame, text="<", command=self.load_previous_data_to_treeview,
                                           bootstyle=INFO)
        self.previous_page_butten.grid(row=0, column=0, padx=20)

        self.current_page_label = Label(pagination_frame, text="1")
        self.current_page_label.grid(row=0, column=1, padx=20)

        self.next_page_butten = Button(pagination_frame, text=">", command=self.load_next_data_to_treeview,
                                       bootstyle=INFO)
        self.next_page_butten.grid(row=0, column=2, padx=20)

    def arrow_butten_clicked(self):
        self.search_entry.delete(0,"end")
        employee_manager = self.manager.back()
        employee_manager.load_data_to_employee_management_treeview()

    def refresh_butten_clicked(self):
        self.data_load_to_treeview()

    @PerformanceLogger
    def data_load_to_treeview(self, page_number=1, page_size=15):
        self.page_size = page_size
        term = self.search_entry.get().strip()
        response= self.employee_business.request_employee(page_number,page_size, term if term else None)

        if response.success:
            for row in self.request_treeview.get_children():
                self.request_treeview.delete(row)

            for index,employee in enumerate(response.data):
                row_number=(page_number-1)*page_size+index+1
                self.request_treeview.insert(
                    "",
                    "end",
                    iid=employee.id,
                    text=str(row_number),
                    values=(
                        employee.firstname,
                        employee.lastname,
                        employee.national_code,
                        employee.username,
                        employee.status_id.name,
                        employee.regester_date
                    )

                )
            return response.data
        else:
            return Messagebox.show_error(response.message,"Failed!")


    def double_clicked(self,event):
        employee_id = self.request_treeview.focus()
        if not employee_id:
            return
        request_approval=self.manager.show_frame("request approval")
        request_approval.set_entry_employee_request(employee_id)
        self.search_entry.delete(0,"end")



    def load_next_data_to_treeview(self):
        current_size = int(self.current_page_label.cget("text"))
        next_page = current_size + 1
        data = self.data_load_to_treeview(next_page)
        self.current_page_label.config(text=str(next_page))
        if not data or len(data) < self.page_size:
            self.next_page_butten.config(state="disabled")

    def load_previous_data_to_treeview(self):
        current_size = int(self.current_page_label.cget("text"))
        previous_page = max(1, current_size - 1)
        self.data_load_to_treeview(previous_page)
        self.current_page_label.config(text=str(previous_page))
        self.next_page_butten.config(state="normal")


    def search_clicked(self):
        self.data_load_to_treeview()


    def on_search_live(self,event):
        self.search_clicked()

    def reject_butten_clicked(self):
        reject_employee = self.manager.show_frame("reject employee")
        reject_employee.data_load_to_treeview()
        self.search_entry.delete(0,"end")













