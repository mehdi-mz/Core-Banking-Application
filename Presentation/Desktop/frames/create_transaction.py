from tkinter.ttk import Combobox
from ttkbootstrap import Frame,Label,Entry,Button,PhotoImage
from ttkbootstrap.style import LIGHT,INFO
from ttkbootstrap.dialogs import Messagebox
from Common.entities.Enums.transaction_types import TransactionTypes

from Common.Decorators.performance_logger_decorator import PerformanceLogger



class CreateTransaction(Frame):
    def __init__(self,window,manager,transaction_business):
        super().__init__(window)


        self.grid_columnconfigure(1,weight=1)

        self.manager=manager
        self.transaction_business=transaction_business

        self.header = Label(self, text="--------------- Create Transaction Form ---------------")
        self.header.grid(row=0, column=0,columnspan=2,pady=(10,20))

        self.arrow_image = PhotoImage(file=r"assets\image\icons8-arrow-30.png").subsample(2, 2)
        self.arrow_butten = Button(self, image=self.arrow_image, command=self.arrow_butten_clicked, bootstyle=LIGHT)
        self.arrow_butten.grid(row=0, column=0, padx=(5, 10),pady=(10,20), sticky="w")

        self.card_to_card_butten = Button(self,text="Card to Card"
                                          ,bootstyle=INFO,command=self.card_to_card_butten_clicked)
        self.card_to_card_butten.grid(row=1,column=1,pady=(0,30),sticky="w")

        self.employee_butten = Button(self, text="In-Branch",bootstyle=INFO,state="disabled")
        self.employee_butten.grid(row=1, column=0, pady=(0, 30),padx=(30,0), sticky="e")

        self.amount_label = Label(self, text="Amount")
        self.amount_label.grid(row=2, column=0, pady=(0, 10), padx=10, sticky="e")

        self.amount_entry = Entry(self)
        self.amount_entry.grid(row=2, column=1, pady=(0, 10), padx=(0, 10), sticky="ew")
        self.amount_entry.bind("<KeyRelease>", self.format_amount)

        self.transaction_type_label = Label(self, text="Type")
        self.transaction_type_label.grid(row=3, column=0, pady=(0, 10), padx=10, sticky="e")

        self.transaction_type_entry = Combobox(self, values=("Deposit","Withdraw"), state="readonly")
        self.transaction_type_entry.grid(row=3, column=1, pady=(0, 10), padx=(0, 10), sticky="ew")

        self.error_label = Label(self, text="")
        self.error_label.grid(row=4, column=0,columnspan=2, pady=(0, 10))

        self.submit_button = Button(self, text="Submit", command=self.submit_transaction_button_clicked)
        self.submit_button.grid(row=5, column=0,columnspan=2, pady=(0, 10), padx=(0, 10))


        self.account_number = None

    @PerformanceLogger
    def submit_transaction_button_clicked(self):
        if not self.amount_entry.get():
            return Messagebox.show_error("Amount cannot be empty.","Amount Error")

        amount = float(self.amount_entry.get().replace(",", ""))

        try:
            transaction_type = TransactionTypes[self.transaction_type_entry.get()]
        except KeyError:
            Messagebox.show_error("Invalid Transaction Type!","Transaction Type Error")
            return

        username = self.manager.current_user.username


        response = self.transaction_business.create_transaction(amount,transaction_type,self.account_number,username)

        if response.success:
            transaction_management = self.manager.back()
            transaction_management.data_load_to_transaction_treeview(self.account_number)
            self.amount_entry.delete(0,"end")
            self.transaction_type_entry.config(state="normal")
            self.transaction_type_entry.delete(0,"end")
            self.transaction_type_entry.config(state="readonly")
            self.error_label.config(text="")
        else:
            Messagebox.show_error(response.message,"Transaction Failed")



    def arrow_butten_clicked(self):
        transaction_management = self.manager.back()
        transaction_management.data_load_to_transaction_treeview(self.account_number)
        self.amount_entry.delete(0, "end")
        self.transaction_type_entry.config(state="normal")
        self.transaction_type_entry.delete(0, "end")
        self.transaction_type_entry.config(state="readonly")
        self.error_label.config(text="")

    def card_to_card_butten_clicked(self):
        card_to_card = self.manager.show_frame("card to card")
        card_to_card.set_account_number(self.account_number)
        self.amount_entry.delete(0, "end")
        self.transaction_type_entry.config(state="normal")
        self.transaction_type_entry.delete(0, "end")
        self.transaction_type_entry.config(state="readonly")
        self.error_label.config(text="")


    def set_account_number(self,account_number):
        self.account_number = account_number

    def format_amount(self, event=None):
        value = self.amount_entry.get()

        value = value.replace(",", "")

        if not value.isdigit():
            self.amount_entry.delete(0, "end")
            self.amount_entry.insert(0, "")
            return

        formatted = f"{int(value):,}"

        self.amount_entry.delete(0, "end")
        self.amount_entry.insert(0, formatted)