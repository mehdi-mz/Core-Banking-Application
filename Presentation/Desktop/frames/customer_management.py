from ttkbootstrap import Frame,Label,Entry,Button,PhotoImage,Treeview
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.style import INFO,LIGHT,DANGER,WARNING
from Common.Decorators.performance_logger_decorator import PerformanceLogger
from tkinter import Toplevel

class CustomerManagementFrame(Frame):
    def __init__(self,window,manager,customer_business):
        super().__init__(window)

        self.customer_business = customer_business
        self.manager = manager

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.header_label = Label(self, text="------------ Customer Manager Form ------------")
        self.header_label.grid(row=0, column=0, columnspan=5, pady=10, padx=10)

        self.arrow_image = PhotoImage(file=r"assets\image\icons8-arrow-30.png").subsample(2, 2)
        self.arrow_butten = Button(self, image=self.arrow_image, command=self.arrow_butten_clicked, bootstyle=LIGHT)
        self.arrow_butten.grid(row=0, column=0, padx=(5, 10), pady=10, sticky="w")

        self.search_entry = Entry(self)
        self.search_entry.grid(row=1, column=0, columnspan=4, pady=(0, 10), padx=10, sticky="ew")
        self.search_entry.bind("<KeyRelease>", self.on_search_live)

        self.search_button = Button(self, text="Search", command=self.search_clicked)
        self.search_button.grid(row=1, column=4, pady=(0, 10), padx=(0, 10), sticky="w")

        self.deactive_customer_button = Button(self, text="Deactive Customer", state="disabled"
                                               ,command=self.deactive_customer_button_clicked, bootstyle=DANGER)
        self.deactive_customer_button.grid(row=2, column=0, pady=(0, 10), padx=10, sticky="ew")

        self.block_customer_button = Button(self, text="Block Customer", bootstyle=WARNING
                                            ,command=self.block_customer_button_clicked, state="disabled")
        self.block_customer_button.grid(row=2, column=1, pady=(0, 10), padx=(0,10), sticky="ew")

        self.update_customer_button = Button(self, text="Update Customer", state="disabled"
                                             , bootstyle=INFO,command=self.update_customer_button_clicked)
        self.update_customer_button.grid(row=2, column=2, pady=(0, 10), padx=(0, 10), sticky="ew")

        self.view_accounts_button = Button(self, text="View Accounts", bootstyle=INFO,
                                           state="disabled",command=self.view_accounts_clicked)
        self.view_accounts_button.grid(row=2, column=3, pady=(0, 10), padx=(0, 10), sticky="ew")

        self.refresh = PhotoImage(file=r"assets\image\icons8-refresh-50-2.png").subsample(2, 2)
        self.refresh_butten = Button(self, image=self.refresh, command=self.refresh_butten_clicked, bootstyle=LIGHT)
        self.refresh_butten.grid(row=2, column=4, padx=(5, 10), pady=(10, 20), sticky="e")

        self.customer_list_treeview = Treeview(self, columns=("firstname_owner",
                                                             "lastname_owner",
                                                              "national_code",
                                                             "phone_number_owner"))

        self.customer_list_treeview.heading("#0", text="#")
        self.customer_list_treeview.heading("#1", text="First Name")
        self.customer_list_treeview.heading("#2", text="Last Name")
        self.customer_list_treeview.heading("#3", text="National Code")
        self.customer_list_treeview.heading("#4", text="Phone Number")

        self.customer_list_treeview.column("#0", width=50,stretch=False)

        for col in self.customer_list_treeview["columns"]:
            self.customer_list_treeview.column(col, width=120, anchor="center")

        self.customer_list_treeview.grid(row=3, column=0, columnspan=5, pady=(0, 10), padx=10, sticky="ewsn")

        self.customer_list_treeview.bind("<<TreeviewSelect>>", self.customer_select)

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

    def customer_select(self, event):
        selection = self.customer_list_treeview.selection()
        if selection:
            self.selected_customer_id = selection[0]
            self.deactive_customer_button.config(state="normal")
            self.block_customer_button.config(state="normal")
            self.update_customer_button.config(state="normal")
            self.view_accounts_button.config(state="normal")
        else:
            self.deactive_customer_button.config(state="disabled")
            self.block_customer_button.config(state="disabled")
            self.update_customer_button.config(state="disabled")
            self.view_accounts_button.config(state="disabled")


    def arrow_butten_clicked(self):
        self.search_entry.delete(0, "end")
        account_management = self.manager.back()
        account_management.load_data_to_account_management_treeview()

    def refresh_butten_clicked(self):
        self.load_data_to_customer_management_treeview()


    @PerformanceLogger
    def load_data_to_customer_management_treeview(self, page_number=1, page_size=15):
        if page_number == 1 :
            self.current_page_label.config(text="1")
            self.next_page_butten.config(state="normal")
        self.page_size = page_size
        term = self.search_entry.get().strip()
        if term:
            response = self.customer_business.get_customers(page_number, page_size, term)
        else:
            response = self.customer_business.get_customers(page_number, page_size)

        if response.success:
            for row in self.customer_list_treeview.get_children():
                self.customer_list_treeview.delete(row)

            for index, customer in enumerate(response.data):
                rownumber = (page_number - 1) * page_size + index + 1
                self.customer_list_treeview.insert(
                    "",
                    "end",
                    iid=customer.customer_id,
                    text=str(rownumber),
                    values=(
                        customer.firstname
                        ,customer.lastname,
                        customer.national_code,
                        customer.phon_number
                    )

                )
            return response.data
        else:
            Messagebox.show_error(response.message, "Failed")

    def load_next_data_to_treeview(self):
        current_size = int(self.current_page_label.cget("text"))
        next_page = current_size + 1
        data = self.load_data_to_customer_management_treeview(next_page)
        self.current_page_label.config(text=str(next_page))
        if not data or len(data) < self.page_size:
            self.next_page_butten.config(state="disabled")

    def load_previous_data_to_treeview(self):
        current_size = int(self.current_page_label.cget("text"))
        previous_page = max(1, current_size - 1)
        self.load_data_to_customer_management_treeview(previous_page)
        self.current_page_label.config(text=str(previous_page))
        self.next_page_butten.config(state="normal")

    def search_clicked(self):
        self.load_data_to_customer_management_treeview()

    def on_search_live(self, event):
        self.search_clicked()

    def view_accounts_clicked(self):
        customer_id = self.customer_list_treeview.selection()[0]
        customer_account = self.manager.show_frame("customer accounts")
        customer_account.load_data_to_account_management_treeview(customer_id)

    def update_customer_button_clicked(self):
        customer_id = self.customer_list_treeview.selection()[0]
        update_customer = self.manager.show_frame("update customer")
        update_customer.set_entry(customer_id)

    def deactive_customer_button_clicked(self):
        self.customer_id = self.selected_customer_id
        self.window = Toplevel(self)

        self.window.title("Deactivated Customer")
        self.window.resizable(False, False)

        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.window.winfo_screenheight() // 2) - (200 // 2)
        y -= 130
        x -= 110
        self.window.geometry(f"650x250+{x}+{y}")


        self.first_name_label = Label(self.window, text="First Name")
        self.first_name_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.first_name_entry = Entry(self.window, state="readonly")
        self.first_name_entry.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="w")

        self.last_name_label = Label(self.window, text="Last Name")
        self.last_name_label.grid(row=0, column=2, padx=10, pady=10, sticky="e")
        self.last_name_entry = Entry(self.window, state="readonly")
        self.last_name_entry.grid(row=0, column=3, padx=(0, 10), pady=10, sticky="w")

        self.national_code_label = Label(self.window, text="National Code")
        self.national_code_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.national_code_entry = Entry(self.window, state="readonly")
        self.national_code_entry.grid(row=1, column=1, padx=(0, 10), pady=10, sticky="w")

        self.butten_deactivated = Button(self.window, text="Deactivated Customer"
                                         ,command=self.butten_deactivated_clicked, bootstyle=DANGER)
        self.butten_deactivated.grid(row=2, column=0, columnspan=4,pady=30)
        self.set_entry(self.customer_id)



    def block_customer_button_clicked(self):
        self.customer_id = self.selected_customer_id
        self.window = Toplevel(self)

        self.window.title("Blocked Customer")
        self.window.resizable(False, False)

        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.window.winfo_screenheight() // 2) - (200 // 2)
        y -= 130
        x -= 110
        self.window.geometry(f"650x250+{x}+{y}")

        self.first_name_label = Label(self.window, text="First Name")
        self.first_name_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.first_name_entry = Entry(self.window, state="readonly")
        self.first_name_entry.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="w")

        self.last_name_label = Label(self.window, text="Last Name")
        self.last_name_label.grid(row=0, column=2, padx=10, pady=10, sticky="e")
        self.last_name_entry = Entry(self.window, state="readonly")
        self.last_name_entry.grid(row=0, column=3, padx=(0, 10), pady=10, sticky="w")

        self.national_code_label = Label(self.window, text="National Code")
        self.national_code_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.national_code_entry = Entry(self.window, state="readonly")
        self.national_code_entry.grid(row=1, column=1, padx=(0, 10), pady=10, sticky="w")

        self.butten_blocked = Button(self.window, text="Blocked Customer"
                                     ,command=self.butten_blocked_clicked, bootstyle=WARNING)
        self.butten_blocked.grid(row=2, column=0, columnspan=4,pady=30)
        self.set_entry(self.customer_id)


    def set_entry(self,customer_id):
        response = self.customer_business.get_customer_by_id(customer_id)
        if response.success:
            self.first_name_entry.config(state="normal")
            self.first_name_entry.delete(0,"end")
            self.first_name_entry.insert(0,response.data.firstname)
            self.first_name_entry.config(state="readonly")

            self.last_name_entry.config(state="normal")
            self.last_name_entry.delete(0, "end")
            self.last_name_entry.insert(0, response.data.lastname)
            self.last_name_entry.config(state="readonly")

            self.national_code_entry.config(state="normal")
            self.national_code_entry.delete(0, "end")
            self.national_code_entry.insert(0, response.data.national_code)
            self.national_code_entry.config(state="readonly")

    def butten_deactivated_clicked(self):
        response = self.customer_business.deactivated_customer(self.customer_id)
        if response.success:
            Messagebox.show_info(response.message,"Success")
            self.window.destroy()
        else:
            Messagebox.show_error(response.message,"Error")
            self.window.destroy()


    def butten_blocked_clicked(self):
        response = self.customer_business.blocked_customer(self.customer_id)
        if response.success:
            Messagebox.show_info(response.message, "Success")
            self.window.destroy()
        else:
            Messagebox.show_error(response.message, "Error")
            self.window.destroy()

