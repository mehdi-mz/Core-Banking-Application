from Common.Repositories.iaccount_repository import IAccountRepository
from Common.DTOs.response import Response


class AccountBusinessLogic:
    def __init__(self,account_repository:IAccountRepository):

        self.account_repository = account_repository


    def get_account_list(self,page_number=1,page_size=15,term=None):
        if term:
            try:
                account_list = self.account_repository.get_account(page_number,page_size,term)
                return Response(True,"", account_list)
            except Exception as e :
                print(f"Exception in get_account_list(term): {e}")
                return Response(False, "Load Account List failed!", None)
        else:
            try:
                account_list = self.account_repository.get_account(page_number, page_size)
                return Response(True,"",account_list)
            except Exception as e :
                print(f"Exception in get_account_list: {e}")
                return Response(False, "Load Account List failed!", None)

    def create_account(self,national_code, status,typee):
        type_value = typee.value
        status_value = status.value

        try:
            row = self.account_repository.create_account(national_code,status_value,type_value)
            if row >= 1:
                return Response(True, "Account was successfully created. ✅", None)
            else:
                return Response(False, "Failed to create account. ❌", None)

        except Exception as e :
            print(f"Exception in create_account: {e}")
            return Response(False, "Database error occurred ❌. Please try again later.", None)


    def get_account_by_id(self,account_number):
        try:
            account = self.account_repository.get_account_by_id(account_number)
            return Response(True,"",account)
        except Exception as e :
            print(f"Exception in get_account_by_id: {e}")
            return Response(False,"Database error occurred ❌. Please try again later.", None)

    def update_account(self,account_number,account_type,account_status):
        account_type_value =account_type.value
        account_status_value = account_status.value

        try:
            row = self.account_repository.update_account(account_number,account_type_value,account_status_value)
            if row == 1:
                return Response(True,"Information has been successfully updated. ✅",None)
            else:
                return Response(False,"Failed to update the information. ❌",None)
        except Exception as e:
            print(f"Exception in update_account: {e}")
            return Response(False, "An error occurred while updating the information. ❌", None)


    def customer_accounts(self,customer_id):
        try:
            accounts = self.account_repository.customer_accounts(customer_id)
            return Response(True,"",accounts)
        except Exception as e :
            print(f"Exception in customer_accounts: {e}")
            return Response(False, "Database error occurred ❌. Please try again later.", None)



