from ttkbootstrap import Frame,Label,Button,PhotoImage,Treeview,Entry
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.style import LIGHT,INFO,SUCCESS,WARNING
from Common.Decorators.performance_logger_decorator import PerformanceLogger
from tkinter import Toplevel



class CustomerAccountsFrame(Frame):
    def __init__(self,window,manager,account_business,customer_business):
        super().__init__(window)

        self.account_bisiness = account_business
        self.customer_business = customer_business
        self.manager=manager

        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.grid_rowconfigure(2,weight=1)

        self.header_label = Label(self, text="------------ Account Manager Form ------------")
        self.header_label.grid(row=0, column=0, columnspan=4, pady=10, padx=10)

        self.arrow_image=PhotoImage(file=r"assets\image\icons8-arrow-30.png").subsample(2,2)
        self.arrow_butten=Button(self,image=self.arrow_image,command=self.arrow_butten_clicked,bootstyle=LIGHT)
        self.arrow_butten.grid(row=0,column=0,padx=(5,10),pady=10,sticky="w")

        self.activated_account_button = Button(self, text="Activated Accounts"
                                            , bootstyle=SUCCESS, command=self.activated_account_clicked)
        self.activated_account_button.grid(row=1, column=0, pady=(0, 10), padx=(0, 10), sticky="ew")


        self.update_account_button = Button(self, text="Update Account",state="disabled"
                                            ,bootstyle=INFO,command=self.update_account_clicked)
        self.update_account_button.grid(row=1, column=1, pady=(0, 10), padx=(0, 10), sticky="ew")


        self.transaction_button = Button(self, text="Transaction",state="disabled"
                                         ,bootstyle=INFO,command=self.transaction_button_clicked)
        self.transaction_button.grid(row=1, column=2, pady=(0, 10), padx=(0, 10), sticky="ew")

        self.refresh = PhotoImage(file=r"assets\image\icons8-refresh-50-2.png").subsample(2, 2)
        self.refresh_butten = Button(self, image=self.refresh, command=self.refresh_butten_clicked, bootstyle=LIGHT)
        self.refresh_butten.grid(row=1, column=3, padx=(5, 10), pady=(10,20), sticky="e")

        self.account_list_treeview=Treeview(self,columns=(  "firstname_owner",
                                                            "lastname_owner",
                                                            "phone_number_owner",
                                                            "account_number",
                                                            "opening_date",
                                                            "account_type",
                                                            "account_status"))

        self.account_list_treeview.heading("#0", text="#")
        self.account_list_treeview.heading("#1", text="First Name")
        self.account_list_treeview.heading("#2", text="Last Name")
        self.account_list_treeview.heading("#3", text="Phone Number")
        self.account_list_treeview.heading("#4", text="Account Number")
        self.account_list_treeview.heading("#5", text="Opening Date")
        self.account_list_treeview.heading("#6", text="Account Type")
        self.account_list_treeview.heading("#7", text="Account Status")


        self.account_list_treeview.column("#0",width=50,stretch=False)

        for col in self.account_list_treeview["columns"]:
            self.account_list_treeview.column(col, width=120, anchor="center")

        self.account_list_treeview.grid(row=2,column=0,columnspan=4,pady=(0,10),padx=10,sticky="ewsn")

        self. account_list_treeview.bind("<<TreeviewSelect>>",self.account_select)




    def account_select(self,event):
        selection = self.account_list_treeview.selection()
        if selection:
            self.update_account_button.config(state="normal")
            self.transaction_button.config(state="normal")
        else:
            self.update_account_button.config(state="disabled")
            self.transaction_button.config(state="disabled")


    def arrow_butten_clicked(self):
        self.manager.back()

    def refresh_butten_clicked(self):
        self.load_data_to_account_management_treeview(self.customer_id)



    @PerformanceLogger
    def load_data_to_account_management_treeview(self,customer_id):
        self.customer_id = customer_id
        response = self.account_bisiness.customer_accounts(customer_id)


        if response.success:
            for row in self.account_list_treeview.get_children():
                self.account_list_treeview.delete(row)

            for index,account in enumerate(response.data):
                self.account_list_treeview.insert(
                    "",
                    "end",
                    iid=account.account_number,
                    text=str(index+1),
                    values=(
                        account.customer.firstname,
                        account.customer.lastname,
                        account.customer.phon_number,
                        account.account_number,
                        account.created_date,
                        account.account_type.name.replace("_"," "),
                        account.account_status.name
                         )

                )
            return response.data
        else:
            Messagebox.show_error(response.message,"Failed")


    @PerformanceLogger
    def transaction_button_clicked(self):

        transaction_frame= self.manager.show_frame("Transaction Manajement")
        account_number = self.account_list_treeview.selection()[0]
        transaction_frame.data_load_to_transaction_treeview(account_number)


    def search_clicked(self):
        self.load_data_to_account_management_treeview()

    def on_search_live(self,event):
        self.search_clicked()



    @PerformanceLogger
    def update_account_clicked(self):
        account_number = self.account_list_treeview.selection()[0]
        update_account = self.manager.show_frame("update account")
        update_account.set_entry(account_number)

    def activated_account_clicked(self):
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

        self.button_activated = Button(self.window, text="Activated Customer"
                                     , command=self.button_activated_clicked, bootstyle=SUCCESS)
        self.button_activated.grid(row=2, column=0, columnspan=4, pady=30)
        self.set_entry(self.customer_id)

    def set_entry(self, customer_id):
        response = self.customer_business.get_customer_by_id(customer_id)
        if response.success:
            self.first_name_entry.config(state="normal")
            self.first_name_entry.delete(0, "end")
            self.first_name_entry.insert(0, response.data.firstname)
            self.first_name_entry.config(state="readonly")

            self.last_name_entry.config(state="normal")
            self.last_name_entry.delete(0, "end")
            self.last_name_entry.insert(0, response.data.lastname)
            self.last_name_entry.config(state="readonly")

            self.national_code_entry.config(state="normal")
            self.national_code_entry.delete(0, "end")
            self.national_code_entry.insert(0, response.data.national_code)
            self.national_code_entry.config(state="readonly")

    def button_activated_clicked(self):
        response = self.customer_business.activated_customer(self.customer_id)
        if response.success:
            Messagebox.show_info(response.message, "Success")
            self.window.destroy()
        else:
            Messagebox.show_error(response.message, "Error")
            self.window.destroy()
