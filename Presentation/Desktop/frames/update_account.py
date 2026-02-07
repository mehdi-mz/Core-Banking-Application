from ttkbootstrap import Frame,Label,Entry,PhotoImage,Combobox,Button
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.style import SUCCESS,LIGHT,WARNING,DANGER
from Common.entities.Enums.account_status import AccountStatus
from Common.entities.Enums.account_types import AccountTypes



class UpdateAccountFrame(Frame):
    def __init__(self,window,manager,account_business):
        super().__init__(window)
        self.manager = manager
        self.account_business = account_business

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)

        self.header_label = Label(self,
                                            text="----------------------- Update Account -----------------------")
        self.header_label.grid(row=0, columnspan=5, column=0, padx=10, pady=10)

        self.image_arrow = PhotoImage(file=r"assets\image\icons8-arrow-30.png").subsample(2, 2)
        self.butten_arrow = Button(self, image=self.image_arrow, command=self.butten_arrow_clicked, bootstyle=LIGHT)
        self.butten_arrow.grid(row=0, column=0, padx=10, pady=(5, 20), sticky="w")

        self.label_firstname = Label(self, text="First Name")
        self.label_firstname.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="e")
        self.entry_firstname = Entry(self,state="readonly")
        self.entry_firstname.grid(row=1, column=1, pady=(0, 10), padx=(0, 10), sticky="ew")

        self.label_lastname = Label(self, text="Last Name")
        self.label_lastname.grid(row=1, column=3, padx=10, pady=(0, 10), sticky="e")
        self.entry_lastname = Entry(self,state="readonly")
        self.entry_lastname.grid(row=1, column=4, pady=(0, 10), padx=(0, 10), sticky="ew")

        self.label_account_number = Label(self, text="Account Number")
        self.label_account_number.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="e")
        self.entry_account_number = Entry(self,state="readonly")
        self.entry_account_number.grid(row=2, column=1, columnspan=4, pady=(0, 10), padx=(0, 10), sticky="ew")

        self.label_type = Label(self, text="Account Type")
        self.label_type.grid(row=3, column=0, pady=(0, 10), padx=10, sticky="e")
        self.account_type = Combobox(self, values=[account_type.name.replace("_"," ") for account_type in AccountTypes],
                                     state="readonly")
        self.account_type.grid(row=3, column=1, columnspan=4, padx=(0, 10), pady=(0, 10), sticky="ew")

        self.label_type = Label(self, text="Account Status")
        self.label_type.grid(row=4, column=0, pady=(0, 10), padx=10, sticky="e")
        self.account_status = Combobox(self, values=[account_status.name for account_status in AccountStatus ], state="readonly")
        self.account_status.grid(row=4, column=1, columnspan=4, padx=(0, 10), pady=(0, 10), sticky="ew")

        self.error_account = Label(self)
        self.error_account.grid(row=5, column=0, columnspan=5, pady=10)

        self.butten_ok = Button(self, text="Ok",command=self.save_update_account_button_clicked,bootstyle=SUCCESS)
        self.butten_ok.grid(row=5, column=0, columnspan=5, pady=20)

    def butten_arrow_clicked(self):
        self.manager.back()


    def save_update_account_button_clicked(self):
        try:
            account_type = AccountTypes[self.account_type.get().replace(" ","_")]
        except KeyError:
            Messagebox.show_error("Invalid Account Type value.","Error")
            return

        try:
            account_status = AccountStatus[self.account_status.get()]
        except KeyError:
            Messagebox.show_error("Invalid Account Status value.","Error")
            return

        response = self.account_business.update_account(self.account_number,account_type,account_status)
        if response.success:
            Messagebox.show_info(response.message,"Success")
            self.manager.back()
        else:
            Messagebox.show_error(response.message,"Error")


    def set_entry(self,account_number):
        response = self.account_business.get_account_by_id(account_number)
        self.account_number = response.data.account_number
        if response.success:
            self.entry_firstname.config(state="normal")
            self.entry_firstname.delete(0,"end")
            self.entry_firstname.insert(0,response.data.customer.firstname)
            self.entry_firstname.config(state="readonly")

            self.entry_lastname.config(state="normal")
            self.entry_lastname.delete(0, "end")
            self.entry_lastname.insert(0, response.data.customer.lastname)
            self.entry_lastname.config(state="readonly")

            self.entry_account_number.config(state="normal")
            self.entry_account_number.delete(0, "end")
            self.entry_account_number.insert(0, response.data.account_number)
            self.entry_account_number.config(state="readonly")

            self.account_type.config(state="normal")
            self.account_type.delete(0, "end")
            self.account_type.insert(0, response.data.account_type.name.replace("_"," "))
            self.account_type.config(state="readonly")

            self.account_status.config(state="normal")
            self.account_status.delete(0, "end")
            if response.data.account_status == AccountStatus.Active:
                self.account_status.insert(0, response.data.account_status.name)
                self.account_status.config(bootstyle=SUCCESS)
            elif  response.data.account_status == AccountStatus.Deactivate:
                self.account_status.insert(0, response.data.account_status.name)
                self.account_status.config(bootstyle=DANGER)
            elif  response.data.account_status == AccountStatus.Block:
                self.account_status.insert(0, response.data.account_status.name)
                self.account_status.config(bootstyle=WARNING)
            self.account_status.config(state="readonly")



