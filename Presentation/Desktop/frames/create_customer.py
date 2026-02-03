from ttkbootstrap import Frame,Label,Entry,Button,PhotoImage,Combobox
from ttkbootstrap.style import LIGHT,DANGER,SUCCESS
from ttkbootstrap.dialogs import Messagebox
from Common.Decorators.performance_logger_decorator import PerformanceLogger
from Common.entities.Enums.account_types import AccountTypes
from Common.entities.Enums.account_status import AccountStatus
from Common.entities.Enums.gender import Gender

class CreateCustomerFrame(Frame):
    def __init__(self,window,manager,customer_bisiness,account_business):
        super().__init__(window)

        self.manager=manager
        self.customer_bisiness =customer_bisiness
        self.account_business = account_business


        self.grid_columnconfigure(1,weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)

        self.header_create_customer=Label(self,text="----------------------- Create Customer -----------------------")
        self.header_create_customer.grid(row=0,columnspan=5,column=0,padx=10,pady=10)

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

        self.label_nationalcode = Label(self, text="National Code")
        self.label_nationalcode.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="e")
        self.entry_nationalcode = Entry(self)
        self.entry_nationalcode.grid(row=2, column=1, columnspan=4, pady=(0, 10), padx=(0, 10), sticky="ew")

        self.label_phon = Label(self, text="Phon Number")
        self.label_phon.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="e")
        self.entry_phon = Entry(self)
        self.entry_phon.grid(row=3, column=1,columnspan=4, pady=(0, 10), padx=(0, 10), sticky="ew")

        self.label_email = Label(self, text="Email")
        self.label_email.grid(row=4, column=0, padx=10, pady=(0, 10), sticky="e")
        self.entry_email = Entry(self)
        self.entry_email.grid(row=4, column=1,columnspan=4, pady=(0, 10), padx=(0, 10), sticky="ew")

        self.label_brithdate = Label(self, text="Brith Date")
        self.label_brithdate.grid(row=5, column=0, padx=10, pady=(0, 10), sticky="e")
        self.entry_brithdate = Entry(self)
        self.entry_brithdate.grid(row=5, column=1,columnspan=4, pady=(0, 10), padx=(0, 10), sticky="ew")



        self.label_gender = Label(self, text="Gender")
        self.label_gender.grid(row=6, column=0, padx=10, pady=(0, 10), sticky="e")
        self.entry_gender = Combobox(self,values=[gender.name for gender in Gender],state="readonly")
        self.entry_gender.grid(row=6, column=1,columnspan=4, padx=(0, 10), sticky="ew")

        self.error_customer=Label(self)
        self.error_customer.grid(row=7,column=0,columnspan=5,pady=10)

        self.butten_save=Button(self,text="Save ✔",command=self.save_button_clicked,bootstyle=SUCCESS)
        self.butten_save.grid(row=9,column=0,columnspan=5,pady=(5,25))

        self.header_create_accounte =Label(self,text="----------------------- Create Account -----------------------")
        self.header_create_accounte.grid(row=10,columnspan=5,column=0,padx=10,pady=(10,25))

        self.label_type = Label(self, text="Account Type")
        self.label_type.grid(row=11, column=0, pady=(0, 10), padx=10, sticky="e")
        self.account_type = Combobox(self, values=[account_type.name.replace("_"," ") for account_type in AccountTypes],
                                     state="readonly")
        self.account_type.grid(row=11, column=1,columnspan=4, padx=(0, 10), pady=(0, 10), sticky="ew")

        self.label_type = Label(self, text="Account Status")
        self.label_type.grid(row=12, column=0, pady=(0, 10), padx=10, sticky="e")
        self.account_status = Combobox(self, values=[account_status.name for account_status in AccountStatus ], state="readonly")
        self.account_status.grid(row=12, column=1,columnspan=4, padx=(0, 10), pady=(0, 10), sticky="ew")

        self.error_account = Label(self)
        self.error_account.grid(row=13, column=0, columnspan=5, pady=10)

        self.butten_ok = Button(self, text="Ok",command=self.butten_ok_clicked)
        self.butten_ok.grid(row=14,column=0,columnspan=5,pady=(0,15))

    @PerformanceLogger
    def save_button_clicked(self):
        firstname=self.entry_firstname.get()
        lastname=self.entry_lastname.get()
        phon_number=self.entry_phon.get()
        national_code=self.entry_nationalcode.get()
        email=self.entry_email.get()
        brith_date=self.entry_brithdate.get()
        gender = Gender[self.entry_gender.get()]

        response = self.customer_bisiness.create_customer(firstname,lastname,national_code,phon_number,email,brith_date,gender)
        if response.success:
            Messagebox.show_info(response.message,"Success")
            self.error_customer.config(text="")
            self.butten_ok.config(state="normal")
            self.butten_save.config(state="disabled")
        elif response.message == "Failed to create customer. ❌" :
            Messagebox.show_error(response.message,"Error")
        else:
            self.error_customer.config(text=response.message,bootstyle=DANGER)

    def butten_ok_clicked(self):

        national_code = self.entry_nationalcode.get()
        try:
            account_type = AccountTypes[self.account_type.get().replace(" ", "_")]
        except KeyError:
            Messagebox.show_error("Invalid Account Type value.","Error")
            return

        try:
            account_status = AccountStatus[self.account_status.get()]
        except KeyError:
            Messagebox.show_error("Invalid Account Status value.","Error")
            return

        response = self.account_business.create_account(national_code,account_status,account_type)
        if response.success:
            Messagebox.show_info(response.message,"Success")
            self.account_type.config(state="normal")
            self.account_type.delete(0, "end")
            self.account_type.config(state="readonly")
            self.account_status.config(state="normal")
            self.account_status.delete(0, "end")
            self.account_status.config(state="readonly")
            account_management =self.manager.back()
            account_management.load_data_to_account_management_treeview()
        else:
            Messagebox.show_error(response.message, "Error")



    def butten_arrow_clicked(self):
        self.manager.back()
        self.error_customer.config(text="")
        self.error_account.config(text="")

    @PerformanceLogger
    def set_entry_create_customer(self,customer=None):
        if customer:
            self.entry_firstname.delete(0,"end")
            self.entry_firstname.insert(0,customer.firstname)

            self.entry_lastname.delete(0,"end")
            self.entry_lastname.insert(0,customer.lastname)

            self.entry_nationalcode.delete(0, "end")
            self.entry_nationalcode.insert(0, customer.national_code)

            self.entry_phon.delete(0,"end")
            self.entry_phon.insert(0,customer.phon_number)

            self.entry_email.delete(0,"end")
            self.entry_email.insert(0,customer.email)

            self.entry_brithdate.delete(0,"end")
            self.entry_brithdate.insert(0,customer.birth_date)

            self.entry_gender.config(state="normal")
            self.entry_gender.delete(0,"end")
            self.entry_gender.insert(0,customer.gender.name)
            self.entry_gender.config(state="readonly")


            self.butten_save.config(state="disabled")
            self.butten_ok.config(state="normal")
        else:
            self.entry_firstname.config(state="normal")
            self.entry_firstname.delete(0,"end")
            self.entry_lastname.config(state="normal")
            self.entry_lastname.delete(0, "end")
            self.entry_nationalcode.config(state="normal")
            self.entry_nationalcode.delete(0, "end")
            self.entry_phon.config(state="normal")
            self.entry_phon.delete(0, "end")
            self.entry_email.config(state="normal")
            self.entry_email.delete(0, "end")
            self.entry_brithdate.config(state="normal")
            self.entry_brithdate.delete(0,"end")
            self.entry_brithdate.insert(0, "1900-01-01")
            self.entry_gender.config(state="normal")
            self.entry_gender.delete(0, "end")
            self.entry_gender.config(state="readonly")
            self.account_type.config(state="normal")
            self.account_type.delete(0,"end")
            self.account_type.config(state="readonly")
            self.account_status.config(state="normal")
            self.account_status.delete(0, "end")
            self.account_status.config(state="readonly")
            self.butten_save.config(state="normal")
            self.butten_ok.config(state="disabled")
