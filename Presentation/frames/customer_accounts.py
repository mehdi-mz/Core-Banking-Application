from tkinter import Toplevel
from ttkbootstrap import Frame,Label,Entry,Button,PhotoImage,Treeview
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.style import LIGHT,INFO,SUCCESS,DANGER
from Common.Decorators.performance_logger_decorator import PerformanceLogger



class CustomerAccountsFrame(Frame):
    def __init__(self,window,manager,account_business,customer_business):
        super().__init__(window)

        self.account_bisiness = account_business
        self.customer_business = customer_business
        self.manager=manager

        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2,weight=1)

        self.header_label = Label(self, text="------------ Account Manager Form ------------")
        self.header_label.grid(row=0, column=0, columnspan=3, pady=10, padx=10)

        self.arrow_image=PhotoImage(file=r"assets\image\icons8-arrow-30.png").subsample(2,2)
        self.arrow_butten=Button(self,image=self.arrow_image,command=self.arrow_butten_clicked,bootstyle=LIGHT)
        self.arrow_butten.grid(row=0,column=0,padx=(5,10),pady=10,sticky="w")


        self.update_account_button = Button(self, text="Update Account",state="disabled"
                                            ,bootstyle=INFO,command=self.update_account_clicked)
        self.update_account_button.grid(row=1, column=0, pady=(0, 10), padx=(0, 10), sticky="ew")


        self.transaction_button = Button(self, text="Transaction",state="disabled"
                                         ,bootstyle=INFO,command=self.transaction_button_clicked)
        self.transaction_button.grid(row=1, column=1, pady=(0, 10), padx=(0, 10), sticky="ew")

        self.refresh = PhotoImage(file=r"assets\image\icons8-refresh-50-2.png").subsample(2, 2)
        self.refresh_butten = Button(self, image=self.refresh, command=self.refresh_butten_clicked, bootstyle=LIGHT)
        self.refresh_butten.grid(row=1, column=2, padx=(5, 10), pady=(10,20), sticky="e")

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

        self.account_list_treeview.grid(row=2,column=0,columnspan=3,pady=(0,10),padx=10,sticky="ewsn")

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
        transaction_frame.data_load_to_transacion_treeview(account_number)


    def search_clicked(self):
        self.load_data_to_account_management_treeview()

    def on_search_live(self,event):
        self.search_clicked()


    def create_account_clicked(self):
        self.window =Toplevel(self)

        self.window.title("Create Account")
        self.window.resizable(False,False)

        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.window.winfo_screenheight() // 2) - (200 // 2)
        y-=130
        x-=110
        self.window.geometry(f"500x200+{x}+{y}")

        self.window.grid_columnconfigure(1,weight=1)

        self.header = Label(self.window,text="Please enter the customer’s national identification number.",bootstyle=INFO)
        self.header.grid(row=0,column=0,columnspan=2,padx=(20,10),pady=(15,30),sticky="w")

        self.label_national_code= Label(self.window,text="National Code")
        self.label_national_code.grid(row=1,column=0,padx=10,pady=10,sticky="e")

        self.entry_national_code = Entry(self.window)
        self.entry_national_code.grid(row=1,column=1,columnspan=2,padx=10,pady=10,sticky="ew")

        self.label_error=Label(self.window)
        self.label_error.grid(row=2,column=0,columnspan=3)

        self.butten_ok = Button(self.window,text="Ok",bootstyle=SUCCESS,command=self.ok_create_account_clicked)
        self.butten_ok.grid(row=3,columnspan=3,column=0,padx=10,pady=10)

    @PerformanceLogger
    def ok_create_account_clicked(self):
        national_code = self.entry_national_code.get()
        response = self.customer_business.get_customer_by_national_code(national_code)
        if response.success:
            self.window.destroy()
            create_customer = self.manager.show_frame("create customer")
            create_customer.set_entry_create_customer(response.data)
        else:
            if response.message =="Customer not found!":
                self.window.destroy()
                create_customer = self.manager.show_frame("create customer")
                create_customer.set_entry_create_customer()
            elif response.message == "Database error occurred. Please try again later.":
                self.window.destroy()
                Messagebox.show_error(response.message,"Failed")
            else:
                self.label_error.config(text=response.message,bootstyle=DANGER)

    @PerformanceLogger
    def update_account_clicked(self):
        account_number = self.account_list_treeview.selection()[0]
        update_accont = self.manager.show_frame("update account")
        update_accont.set_entry(account_number)

    @PerformanceLogger
    def show_customers_clicked(self):
        customer_management = self.manager.show_frame("customer management")
        customer_management.load_data_to_customer_management_treeview()
