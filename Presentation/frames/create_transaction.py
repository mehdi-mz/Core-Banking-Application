from tkinter.ttk import Combobox
from ttkbootstrap import Frame,Label,Entry,Button,PhotoImage
from ttkbootstrap.style import DANGER,LIGHT
from ttkbootstrap.dialogs import Messagebox

from Common.Decorators.performance_logger_decorator import PerformanceLogger


from Common.entities.Enums.transaction_types import TransactionTypes

class CreateTransation(Frame):
    def __init__(self,window,manager,transaction_business):
        super().__init__(window)


        self.grid_columnconfigure(1,weight=1)

        self.manager=manager
        self.transaction_business=transaction_business

        self.header = Label(self, text="--------------- Create Transaction Form ---------------")
        self.header.grid(row=0, column=0,columnspan=2, pady=10)

        self.arrow_image = PhotoImage(file=r"assets\image\icons8-arrow-30.png").subsample(2, 2)
        self.arrow_butten = Button(self, image=self.arrow_image, command=self.arrow_butten_clicked, bootstyle=LIGHT)
        self.arrow_butten.grid(row=0, column=0, padx=(5, 10), pady=10, sticky="w")

        self.amount_label = Label(self, text="Amount")
        self.amount_label.grid(row=1, column=0, pady=(0, 10), padx=10, sticky="e")

        self.amount_entry = Entry(self)
        self.amount_entry.grid(row=1, column=1, pady=(0, 10), padx=(0, 10), sticky="ew")
        self.amount_entry.bind("<KeyRelease>", self.format_amount)

        self.transaction_type_label = Label(self, text="Type")
        self.transaction_type_label.grid(row=2, column=0, pady=(0, 10), padx=10, sticky="e")

        self.transaction_type_entry = Combobox(self, values=("1-Deposit","2-Withdraw"), state="readonly")
        self.transaction_type_entry.grid(row=2, column=1, pady=(0, 10), padx=(0, 10), sticky="ew")

        self.erorr_label = Label(self, text="")
        self.erorr_label.grid(row=3, column=0,columnspan=2, pady=(0, 10))

        self.submit_button = Button(self, text="Submit", command=self.submit_transaction_button_clicked)
        self.submit_button.grid(row=4, column=0,columnspan=2, pady=(0, 10), padx=(0, 10))


        self.account_number = None

    @PerformanceLogger
    def submit_transaction_button_clicked(self):
        amount = float(self.amount_entry.get().replace(",", ""))

        if not self.transaction_type_entry.get():
            self.erorr_label.config(text="Please enter the transaction type.",bootstyle=DANGER)


        transaction_type = TransactionTypes(int(self.transaction_type_entry.get().split("-")[0]))

        username = self.manager.current_user.username


        response = self.transaction_business.create_transaction(amount,transaction_type,self.account_number,username)

        if response.success:

            transaction_manajement = self.manager.back()
            transaction_manajement.data_load_to_transacion_treeview(self.account_number)
            self.amount_entry.delete(0,"end")
            self.transaction_type_entry.config(state="normal")
            self.transaction_type_entry.delete(0,"end")
            self.transaction_type_entry.config(state="readonly")
            self.erorr_label.config(text="")
        else:
            Messagebox.show_error(response.message,"Transaction Failed")



    def arrow_butten_clicked(self):
        create_transaction= self.manager.back()
        self.amount_entry.delete(0, "end")
        self.transaction_type_entry.config(state="normal")
        self.transaction_type_entry.delete(0, "end")
        self.transaction_type_entry.config(state="readonly")
        self.erorr_label.config(text="")

    def set_account_number(self,account_number):
        self.account_number = account_number

    def format_amount(self, event=None):
        value = self.amount_entry.get()

        value = value.replace(",", "")

        if not value.isdigit():
            self.amount_entry.delete(0, "end")
            self.amount_entry.insert(0, "".join(filter(str.isdigit, value)))
            return

        if value == "":
            return
        formatted = f"{int(value):,}"

        self.amount_entry.delete(0, "end")
        self.amount_entry.insert(0, formatted)