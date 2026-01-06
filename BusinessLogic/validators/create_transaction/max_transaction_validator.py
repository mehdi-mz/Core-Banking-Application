from BusinessLogic.validators.base_handler import BaseHandler
from Common.entities.Enums.transaction_types import TransactionTypes


class MaxTransactionValidator(BaseHandler):
    def handel(self, request):
        if request.max_transaction >= 500000 and request.transaction_type == TransactionTypes.Withdraw :
            raise ValueError("You have reached your withdrawal limit.")

        if self.next_handler:
            self.next_handler.handel(request)