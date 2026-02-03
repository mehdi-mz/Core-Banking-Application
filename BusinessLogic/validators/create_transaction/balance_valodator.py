from BusinessLogic.validators.base_handler import BaseHandler
from Common.entities.Enums.transaction_types import TransactionTypes

class BalanceValidator(BaseHandler):
    def handel(self, request):
        if request.balance <= request.transaction_amount and( request.transaction_type == TransactionTypes.Withdraw
                                                              or request.transaction_type == TransactionTypes.Card_To_Card_Out):
            raise ValueError("Balance not enough!")


        if self.next_handler:
            self.next_handler.handel(request)
