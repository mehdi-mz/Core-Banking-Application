from tkinter import Toplevel
from ttkbootstrap import Frame,Label,Entry,Button,PhotoImage,Treeview
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.style import LIGHT,INFO,SUCCESS,DANGER
from Common.Decorators.performance_logger_decorator import PerformanceLogger



class AccountManagmentFrame(Frame):
    def __init__(self,window,manager,account_business,customer_business):
        super().__init__(window)

        self.account_bisiness = account_business
        self.customer_business = customer_business
        self.manager=manager

        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(3,weight=1)

        self.header_label = Label(self, text="------------ Account Manager Form ------------")
        self.header_label.grid(row=0, column=0, columnspan=5, pady=10, padx=10)

        self.arrow_image=PhotoImage(file=r"assets\image\icons8-arrow-30.png").subsample(2,2)
        self.arrow_butten=Button(self,image=self.arrow_image,command=self.arrow_butten_clicked,bootstyle=LIGHT)
        self.arrow_butten.grid(row=0,column=0,padx=(5,10),pady=10,sticky="w")

        self.search_entry = Entry(self)
        self.search_entry.grid(row=1, column=0, columnspan=4, pady=(0, 10), padx=10, sticky="ew")
        self.search_entry.bind("<KeyRelease>", self.on_search_live)

        self.search_button = Button(self, text="Search",command=self.search_clicked)
        self.search_button.grid(row=1, column=4, pady=(0, 10), padx=(0, 10), sticky="w")

        self.show_customers_button = Button(self, text="Show Customers", bootstyle=INFO,command=self.show_customers_clicked)
        self.show_customers_button.grid(row=2, column=0, pady=(0, 10), padx=10, sticky="ew")

        self.create_account_button = Button(self, text="Create Account", bootstyle=INFO,
                                            command=self.create_account_clicked)
        self.create_account_button.grid(row=2, column=1, pady=(0, 10), padx=(0,10), sticky="ew")

        self.update_account_button = Button(self, text="Update Account",state="disabled"
                                            ,bootstyle=INFO,command=self.update_account_clicked)
        self.update_account_button.grid(row=2, column=2, pady=(0, 10), padx=(0, 10), sticky="ew")


        self.transaction_button = Button(self, text="Transaction",state="disabled"
                                         ,bootstyle=INFO,command=self.transaction_button_clicked)
        self.transaction_button.grid(row=2, column=3, pady=(0, 10), padx=(0, 10), sticky="ew")

        self.refresh = PhotoImage(file=r"assets\image\icons8-refresh-50-2.png").subsample(3, 3)
        self.refresh_butten = Button(self, image=self.refresh, command=self.refresh_butten_clicked, bootstyle=LIGHT)
        self.refresh_butten.grid(row=2, column=4, padx=(5, 10), pady=(10, 20), sticky="e")

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
        # self.account_list_treeview.heading("#7", text="Balance")

        self.account_list_treeview.column("#0",width=50,stretch=False)

        for col in self.account_list_treeview["columns"]:
            self.account_list_treeview.column(col, width=120, anchor="center")


        self.account_list_treeview.grid(row=3,column=0,columnspan=5,pady=(0,10),padx=10,sticky="ewsn")

        self. account_list_treeview.bind("<<TreeviewSelect>>",self.account_select)


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



    def account_select(self,event):
        selection = self.account_list_treeview.selection()
        if selection:
            self.update_account_button.config(state="normal")
            self.transaction_button.config(state="normal")
        else:
            self.update_account_button.config(state="disabled")
            self.transaction_button.config(state="disabled")


    def arrow_butten_clicked(self):
        self.search_entry.delete(0,"end")
        self.manager.back()

    def refresh_butten_clicked(self):
        self.load_data_to_account_management_treeview()



    @PerformanceLogger
    def load_data_to_account_management_treeview(self,page_number=1,page_size=15):
        if page_number == 1 :
            self.current_page_label.config(text="1")
            self.next_page_butten.config(state="normal")
        self.page_size = page_size
        term = self.search_entry.get().strip()
        if term:
            response = self.account_bisiness.get_account_list(page_number, page_size,term)
        else:
            response = self.account_bisiness.get_account_list(page_number,page_size)



        if response.success:
            for row in self.account_list_treeview.get_children():
                self.account_list_treeview.delete(row)

            for index,account in enumerate(response.data):
                row_number=(page_number-1)*page_size+index+1
                self.account_list_treeview.insert(
                    "",
                    "end",
                    iid=account.account_number,
                    text=str(row_number),
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


    def load_next_data_to_treeview(self):
        current_size=int(self.current_page_label.cget("text"))
        next_page=current_size+1
        data = self.load_data_to_account_management_treeview(next_page)
        self.current_page_label.config(text=str(next_page))
        if  not data  or len(data) < self.page_size :
            self.next_page_butten.config(state="disabled")

    def load_previous_data_to_treeview(self):
        current_size=int(self.current_page_label.cget("text"))
        previous_page=max(1,current_size-1)
        self.load_data_to_account_management_treeview(previous_page)
        self.current_page_label.config(text=str(previous_page))
        self.next_page_butten.config(state="normal")


    @PerformanceLogger
    def transaction_button_clicked(self):

        transaction_frame= self.manager.show_frame("Transaction Manajement")
        account_number = self.account_list_treeview.selection()[0]
        transaction_frame.data_load_to_transaction_treeview(account_number)


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

    def show_customers_clicked(self):
        customer_management = self.manager.show_frame("customer management")
        customer_management.load_data_to_customer_management_treeview()
































