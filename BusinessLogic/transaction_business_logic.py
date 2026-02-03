from Common.Repositories.itransaction_repository import ITransactionRepository
from Common.Repositories.iaccount_repository import IAccountRepository
from Common.Repositories.icustomer_repository import ICustomerRepository
from Common.DTOs.response import Response
from Common.entities.transaction import Transaction
from reportlab.platypus import SimpleDocTemplate, Paragraph,Image,Table,Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os
from BusinessLogic.validators.create_transaction.create_transaction_request import CreateTransactionRequest
from BusinessLogic.validators.create_transaction.account_status_validator import AccountStatusValidator
from BusinessLogic.validators.create_transaction.positive_amount_validator import PositiveAmountValidator
from BusinessLogic.validators.create_transaction.balance_valodator import BalanceValidator
from BusinessLogic.validators.create_transaction.max_transaction_validator import MaxTransactionValidator
from BusinessLogic.validators.create_transaction.card_status_validator import CardStatusValidator
from datetime import datetime



class TransactionBusinessLogic:
    def __init__(self,transaction_repository : ITransactionRepository,
                      account_repository : IAccountRepository,
                       customer_repository : ICustomerRepository):

        self.transaction_repository = transaction_repository
        self.account_repository = account_repository
        self.customer_repository = customer_repository


    def get_transaction_list(self,account_number:int,page_number=1,page_size=15):
        try:
            transaction_list=self.transaction_repository.get_transactions(account_number , page_number,page_size)
            return Response(True,"",transaction_list)
        except Exception as e:
            print(f"Exception in get_transaction_list: {e}")
            return Response(False,"Transaction Load Failed!",None)



    def get_all_transaction(self,account_number:int):
        try:
            transaction_list=self.transaction_repository.get_all_transactions(account_number)
            return Response(True,"",transaction_list)
        except Exception as e :
            print(f"Exception in get_all_transaction: {e}")
            return Response(False,"Transaction Load Failed!",None)



    def export_pdf_transaction(self,account_number:int,file_path):
        if not file_path:
            return Response(False, "File path is required", None)

        response = self.get_all_transaction(account_number)

        if response.success:
            try:
                 name_customer = self.customer_repository.get_customer_by_account_number(account_number)
            except Exception as e :
                print(f"Exception in name customer to pdf: {e}")
                return Response(False, "name customer to pdf Failed!", None)

            total_balance = self.sum_balance(account_number)
            total_balance_format=f"{total_balance:,.2f}"

            elements = []
            doc = SimpleDocTemplate(file_path)                # یه فایل پی ادی اف آماده میکنه  <--------------------
            styles = getSampleStyleSheet()                      # یه سری فونت بر می گردونه <-----------------------

            left_style = styles["Normal"]
            left_style.fontSize =18
            left_style.leading =14

            name_paragraph = Paragraph(text=f"Name : {name_customer.customer.firstname} {name_customer.customer.lastname}",
                                      style=left_style)

            national_code_paragraph = Paragraph(text=f"National Code : {name_customer.customer.national_code}",
                                      style=left_style)

            doc_paragraph = Paragraph(text=f"Transaction Report (Balance:{total_balance_format})",
                                      style=styles["Title"])                # متن داخل پی دی اف و فونتش  <----------

            logo_path = r"assets\image\2048px-Bank_Melli_Iran_New_Logo.png"
            logo = Image(logo_path, width=100, height=100)
            logo.hAlign = "RIGHT"
            row_data = [(index+1,r.account_number,f"{r.old_balance:,.2f}",f"{r.amount:,.2f}",
                         r.transaction_type.name.replace("_"," "),r.card,r.transaction_time) for index,r in enumerate(response.data)]
            data = [("#","Account Number","Balance before transaction","Amount",
                     "Transaction Type","Card Number","Transaction Time")] + row_data
            table= Table(data)

            table_style = [
                ('BACKGROUND', (0, 0), (-1, 0), '#dcdcdc'),
                ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),

                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

                ('GRID', (0, 0), (-1, -1), 0.5, '#000000'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),

                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('TOPPADDING', (0, 0), (-1, 0), 8),
            ]

            table.setStyle(table_style)



            elements.append(logo)
            elements.append(name_paragraph)
            elements.append(Spacer(0, 12))
            elements.append(national_code_paragraph)
            elements.append(Spacer(0, 12))
            elements.append(doc_paragraph)
            elements.append(Spacer(1,20))
            elements.append(table)

            doc.build(elements)

            os.startfile(file_path)

            return Response(True,"Export successful",None)
        else:
            return Response(False,"Export Pdf Transaction Failed!",None)

    def create_transaction(self,amount, transaction_type, account_number,username,card=None):

        if card:
            account = self.account_repository.get_account_by_id(account_number)
            account_card = self.account_repository.get_account_by_id(card)
            balance = self.transaction_repository.sum_balance(account_number)
            daily_transaction = self.transaction_repository.get_daily_transactions(account_number)
            max_daily_transaction = sum(f.amount for f in daily_transaction)
            request = CreateTransactionRequest(account, amount, balance, transaction_type, max_daily_transaction,
                                               account_card)

            positive_validator = PositiveAmountValidator()
            account_validator = AccountStatusValidator()
            card_status_validator = CardStatusValidator()
            balance_validator = BalanceValidator()
            max_transaction = MaxTransactionValidator()

            positive_validator.set_next(account_validator)
            account_validator.set_next(card_status_validator)
            card_status_validator.set_next(balance_validator)
            balance_validator.set_next(max_transaction)

            try:
                positive_validator.handel(request)

            except ValueError as error:
                return Response(False, error.args[0], None)

            else:
                transaction_type_value = transaction_type.value
                try:
                    old_balance = self.transaction_repository.sum_balance(account_number)
                    old_balance_card = self.transaction_repository.sum_balance(card)
                    new_transaction = Transaction(None, account_number, old_balance, amount, transaction_type_value,
                                                  username, card, datetime.now())
                    self.transaction_repository.card_to_card(new_transaction, old_balance_card)
                    return Response(True, "", None)
                except Exception as e:
                    print(f"Exception in card to card: {e}")
                    return Response(False, "Database Exception", None)
        else:
            account = self.account_repository.get_account_by_id(account_number)
            balance = self.transaction_repository.sum_balance(account_number)
            daily_transaction = self.transaction_repository.get_daily_transactions(account_number)
            max_daily_transaction = sum(f.amount  for f in daily_transaction)
            request = CreateTransactionRequest(account,amount,balance,transaction_type,max_daily_transaction)

            positive_validator = PositiveAmountValidator()
            account_validator = AccountStatusValidator()
            balance_validator = BalanceValidator()
            max_transaction = MaxTransactionValidator()

            positive_validator.set_next(account_validator)
            account_validator.set_next(balance_validator)
            balance_validator.set_next(max_transaction)

            try:
                positive_validator.handel(request)

            except ValueError as error:
                return  Response(False,error.args[0],None)

            else:
                transaction_type_value = transaction_type.value
                try:
                    old_balance = self.transaction_repository.sum_balance(account_number)
                    new_transaction = Transaction(None,account_number,old_balance,amount,
                                                  transaction_type_value,username,None,datetime.now())
                    self.transaction_repository.insert_transaction(new_transaction)
                    return Response(True,"",None)
                except Exception as e :
                    print(f"Exception in create_transaction: {e}")
                    return Response(False,"Database Exception",None)

    def sum_balance(self,account_number:int):
        balance = self.transaction_repository.sum_balance(account_number)
        return balance





