from BusinessLogic.validators.base_handler import BaseHandler
from Common.entities.Enums.transaction_types import TransactionTypes


class BalanceValidator(BaseHandler):
    def handel(self, request):
        if request.balance <= request.transaction_amount and request.transaction_type == TransactionTypes.Withdraw:
            raise ValueError("Balance not enough!")

        if self.next_handler:
            self.next_handler.handel(request)
