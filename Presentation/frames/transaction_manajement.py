from ttkbootstrap import Frame,Label,Button,PhotoImage,Treeview
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.style import LIGHT,SUCCESS,INFO
from tkinter import filedialog
from Common.Decorators.performance_logger_decorator import PerformanceLogger
import tkinter.font as tkFont



class TransactionManajementFrame(Frame):
    def __init__(self,window,manager,trancsaction_business):
        super().__init__(window)


        self.transaction_business = trancsaction_business
        self.manager = manager


        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1,weight=1)

        self.grid_rowconfigure(3,weight=1)



        self.header_label = Label(self, text="----------- Transaction Manager Form -----------")
        self.header_label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        self.arrow_image = PhotoImage(file=r"assets\image\icons8-arrow-30.png").subsample(2, 2)
        self.arrow_butten = Button(self, image=self.arrow_image, command=self.arrow_butten_clicked, bootstyle=LIGHT)
        self.arrow_butten.grid(row=0, column=0, padx=(5, 10), pady=10, sticky="w")

        self.big_font = tkFont.Font(family="Helvetica", size=18, weight="bold")

        self.account_balance = Label(self,bootstyle=SUCCESS,font=self.big_font)
        self.account_balance.grid(row=1, column=0, columnspan=2, pady=15, padx=10,sticky="w")

        self.label_account_number = Label(self, bootstyle=INFO, font=self.big_font)
        self.label_account_number.grid(row=1, column=1, columnspan=2, pady=15, padx=10, sticky="w")

        self.create_transaction_button = Button(self, text="Create Transaction",command=self.create_transaction_button_clicked)
        self.create_transaction_button.grid(row=2, column=0, pady=(0, 10), padx=10, sticky="ew")

        self.export_pdf_transaction_button = Button(self, text="Export to PDF",command=self.export_pdf_transaction_button_clicked)

        self.export_pdf_transaction_button.grid(row=2, column=1, pady=(0, 10), padx=10, sticky="ew")



        self.transaction_treeview=Treeview(self,columns=(
                                                         "old_balance",
                                                         "amount",
                                                         "transaction_type",
                                                         "update_time"
                                                         ))
        self.transaction_treeview.grid(row=3,column=0,columnspan=2,pady=(0,10),padx=10,sticky="snew")
        self.transaction_treeview.column("#0",width=50)
        self.transaction_treeview.heading("#0",text="#")
        self.transaction_treeview.heading("#1",text="Balance before transaction")
        self.transaction_treeview.heading("#2",text="Amount")
        self.transaction_treeview.heading("#3",text="Transaction Type")
        self.transaction_treeview.heading("#4",text="Transaction Time")

        self.transaction_treeview.column("#0",width=50,stretch=False)

        for col in self.transaction_treeview["columns"]:
            self.transaction_treeview.column(col, width=120, anchor="center")

        self.acount_number = None


        pagination_frame = Frame(self)
        pagination_frame.grid(row=4, column=0, columnspan=2, pady=(0, 10))

        self.previous_page_butten = Button(pagination_frame, text="<", command=self.load_previous_data_to_treeview,
                                           bootstyle=INFO)
        self.previous_page_butten.grid(row=0, column=0, padx=20)

        self.current_page_label = Label(pagination_frame, text="1")
        self.current_page_label.grid(row=0, column=1, padx=20)

        self.next_page_butten = Button(pagination_frame, text=">", command=self.load_next_data_to_treeview,
                                       bootstyle=INFO)
        self.next_page_butten.grid(row=0, column=2, padx=20)

    def arrow_butten_clicked(self):
        self.manager.back()

    @PerformanceLogger
    def data_load_to_transacion_treeview(self,account_number:int, page_number=1, page_size=15):
        if page_number == 1 :
            self.current_page_label.config(text="1")
            self.next_page_butten.config(state="normal")

        self.page_size = page_size
        self.acount_number = account_number

        response= self.transaction_business.get_transaction_list(account_number,page_number,page_size)

        self.label_account_number.config(text=f"Account Number: {self.acount_number}")


        if response.success:
            balance = self.transaction_business.sum_balance(account_number)
            balance_format = f"{balance:,.2f}"
            self.account_balance.config(text=f"Balance: {balance_format} T")

            for row in self.transaction_treeview.get_children():
                self.transaction_treeview.delete(row)

            for index,transaction in enumerate(response.data):
                rownumber = (page_number - 1) * page_size + index + 1
                self.transaction_treeview.insert(
                    "",
                    "end",
                    iid=transaction.id,
                    text=str(rownumber),
                    values=(
                        f"{transaction.old_balance:,.2f}",
                        f"{transaction.amount:,.2f}",
                        transaction.transaction_type.name,
                        transaction.transaction_time
                    )

                )
        else:
            Messagebox.show_error("Transaction Failed!",response.message)

    @PerformanceLogger
    def export_pdf_transaction_button_clicked(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.PDF",)]
                                                 , title="Save as Transaction Report")
        if file_path:
            response = self.transaction_business.export_pdf_transaction(self.acount_number,file_path)
            if not  response.success :
                Messagebox.show_error(response.message,"erorr")


    @PerformanceLogger
    def create_transaction_button_clicked(self):
        create_transaction = self.manager.show_frame("create transation")
        create_transaction.set_account_number(self.acount_number)


    def load_next_data_to_treeview(self):
        current_size=int(self.current_page_label.cget("text"))
        next_page=current_size+1
        data = self.data_load_to_transacion_treeview(self.acount_number,next_page)
        self.current_page_label.config(text=str(next_page))
        if  not data  or len(data) < self.page_size :
            self.next_page_butten.config(state="disabled")

    def load_previous_data_to_treeview(self):
        current_size=int(self.current_page_label.cget("text"))
        previous_page=max(1,current_size-1)
        self.data_load_to_transacion_treeview(self.acount_number,previous_page)
        self.current_page_label.config(text=str(previous_page))
        self.next_page_butten.config(state="normal")
