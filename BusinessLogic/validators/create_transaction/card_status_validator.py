from BusinessLogic.validators.base_handler import BaseHandler
from Common.entities.Enums.account_status import AccountStatus

class CardStatusValidator(BaseHandler):


    def handel(self, request):
        if request.card.account_status == AccountStatus.Deactivate:
            raise ValueError("Card is Deactivate. Cannot create a transaction. ❌")

        if request.card.account_status == AccountStatus.Block:
            raise ValueError("Card is Blocked. Cannot create a transaction. ❌")

        if self.next_handler:
            self.next_handler.handel(request)

