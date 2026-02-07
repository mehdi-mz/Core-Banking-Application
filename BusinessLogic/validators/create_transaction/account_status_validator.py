from BusinessLogic.validators.base_handler import BaseHandler
from Common.entities.Enums.account_status import AccountStatus

class AccountStatusValidator(BaseHandler):


    def handel(self, request):
        if request.account.account_status == AccountStatus.Deactivate:
            raise ValueError("Account is Deactivate. Cannot create a transaction. ❌")

        if request.account.account_status == AccountStatus.Block:
            raise ValueError("Account is Blocked. Cannot create a transaction. ❌")

        if self.next_handler:
            self.next_handler.handel(request)

