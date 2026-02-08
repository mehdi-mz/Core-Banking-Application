from ttkbootstrap import Frame,Label,Entry,Button,PhotoImage
from ttkbootstrap.style import DANGER,LIGHT,SUCCESS,INFO
from ttkbootstrap.dialogs import Messagebox
from Common.entities.Enums.transaction_types import TransactionTypes

from Common.Decorators.performance_logger_decorator import PerformanceLogger


class TransferFromCard(Frame):
    def __init__(self,window,manager,transaction_business,customer_business):
        super().__init__(window)


        self.grid_columnconfigure(1,weight=1)

        self.manager=manager
        self.transaction_business=transaction_business
        self.customer_business =customer_business

        self.header = Label(self, text="--------------- Card to Card Form ---------------")
        self.header.grid(row=0, column=0,columnspan=2, pady=(10,20))

        self.arrow_image = PhotoImage(file=r"assets\image\icons8-arrow-30.png").subsample(2, 2)
        self.arrow_butten = Button(self, image=self.arrow_image, command=self.arrow_butten_clicked, bootstyle=LIGHT)
        self.arrow_butten.grid(row=0, column=0, padx=(5, 10), pady=(10,20), sticky="w")

        self.card_to_card_butten = Button(self, text="Card to Card",bootstyle=INFO,state="disabled")
        self.card_to_card_butten.grid(row=1, column=1, pady=(0, 30), sticky="w")

        self.employee_butten = Button(self, text="In-Branch",bootstyle=INFO, command=self.in_branch_butten_clicked)
        self.employee_butten.grid(row=1, column=0,padx=(10,0), pady=(0, 30), sticky="e")

        self.account_number_label = Label(self, text="Account Number")
        self.account_number_label.grid(row=2, column=0, pady=(0, 10), padx=10, sticky="e")

        self.account_number_entry = Entry(self)
        self.account_number_entry.grid(row=2, column=1, pady=(0, 10), padx=(0, 10), sticky="ew")
        self.account_number_entry.bind("<KeyRelease>", self.int_account_number)

        self.amount_label = Label(self, text="Amount")
        self.amount_label.grid(row=3, column=0, pady=(0, 10), padx=10, sticky="e")

        self.amount_entry = Entry(self)
        self.amount_entry.grid(row=3, column=1, pady=(0, 10), padx=(0, 10), sticky="ew")
        self.amount_entry.bind("<KeyRelease>", self.format_amount)


        self.error_label = Label(self, text="")
        self.error_label.grid(row=4, column=0,columnspan=2, pady=(0, 10))

        self.submit_button = Button(self, text="Submit", command=self.submit_transaction_button_clicked)
        self.submit_button.grid(row=5, column=0,columnspan=2, pady=(0, 10), padx=(0, 10))

        self.full_name_label = Label(self,text="Name Account")
        self.full_name_label.grid(row=6,column=0,pady=10,padx=10,sticky="e")

        self.full_name = Entry(self,state="readonly",bootstyle=LIGHT)
        self.full_name.grid(row=6,column=1,padx=(0,10),pady=10,sticky="ew")

        self.ok_button = Button(self, text="Ok",state="disabled",bootstyle=SUCCESS
                                , command=self.ok_button_card_to_card_clicked)
        self.ok_button.grid(row=7, column=0, columnspan=2, pady=10, padx=(0, 10))


        self.account_number = None

    @PerformanceLogger
    def submit_transaction_button_clicked(self):

        self.card = self.account_number_entry.get()
        self.amount = self.amount_entry.get()


        if self.amount:
            response = self.customer_business.get_customer_by_account_number(self.card)
            if response.success:
                fullname=f"{response.data.customer.firstname} {response.data.customer.lastname} ---> {self.amount}"
                self.full_name.config(state="normal",bootstyle=SUCCESS)
                self.full_name.insert(0,fullname)
                self.full_name.config(state="readonly")
                self.ok_button.config(state="normal")
                self.submit_button.config(state="disabled")
                self.amount_entry.config(state="readonly")
                self.account_number_entry.config(state="readonly")
                self.error_label.config(text="")

            else:
                self.error_label.config(text=response.message,bootstyle=DANGER)
        else:
            self.error_label.config(text="Amount cannot be empty.", bootstyle=DANGER)

    @PerformanceLogger
    def ok_button_card_to_card_clicked(self):
        username = self.manager.current_user.username
        transaction_type = TransactionTypes.Card_To_Card_Out
        amount = float(self.amount.replace(",", ""))

        response = self.transaction_business.create_transaction(amount,transaction_type,self.account_number,username,self.card)

        if response.success:
            self.manager.back()
            self.amount_entry.config(state="normal")
            self.account_number_entry.config(state="normal")
            self.amount_entry.delete(0,"end")
            self.account_number_entry.delete(0,"end")
            self.error_label.config(text="")
            self.submit_button.config(state="normal")
            self.ok_button.config(state="disabled")
            self.full_name.config(state="normal",bootstyle=LIGHT)
            self.full_name.delete(0,"end")
            self.full_name.config(state="readonly")
        else:
            Messagebox.show_error(response.message,"Transaction Failed")

    def in_branch_butten_clicked(self):
        self.manager.back()
        self.amount_entry.config(state="normal")
        self.account_number_entry.config(state="normal")
        self.amount_entry.delete(0, "end")
        self.account_number_entry.delete(0, "end")
        self.error_label.config(text="")
        self.full_name.config(state="normal", bootstyle=LIGHT)
        self.full_name.delete(0, "end")
        self.full_name.config(state="readonly")
        self.submit_button.config(state="normal")
        self.ok_button.config(state="disabled")



    def arrow_butten_clicked(self):
        self.manager.back()
        self.amount_entry.config(state="normal")
        self.account_number_entry.config(state="normal")
        self.amount_entry.delete(0, "end")
        self.account_number_entry.delete(0, "end")
        self.error_label.config(text="")
        self.full_name.config(state="normal",bootstyle=LIGHT)
        self.full_name.delete(0, "end")
        self.full_name.config(state="readonly")
        self.submit_button.config(state="normal")
        self.ok_button.config(state="disabled")

    def set_account_number(self,account_number):
        self.account_number = account_number

    def format_amount(self, event=None):
        value = self.amount_entry.get()

        value = value.replace(",", "")

        if not value.isdigit():
            self.amount_entry.delete(0, "end")
            # self.amount_entry.insert(0, "".join(filter(str.isdigit, value)))
            self.amount_entry.insert(0, "")
            return

        # if value == "":
        #     return

        formatted = f"{int(value):,}"

        self.amount_entry.delete(0, "end")
        self.amount_entry.insert(0, formatted)

    def int_account_number(self, event=None):
        value = self.account_number_entry.get()
        if not value.isdigit():
            self.amount_entry.delete(0, "end")
            self.amount_entry.insert(0, "")
            return