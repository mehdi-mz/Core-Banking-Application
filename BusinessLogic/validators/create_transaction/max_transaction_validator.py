from BusinessLogic.validators.base_handler import BaseHandler
from Common.entities.Enums.transaction_types import TransactionTypes



class MaxTransactionValidator(BaseHandler):
    def handel(self, request):
        if request.transaction_amount > 50000000 and (request.transaction_type == TransactionTypes.Withdraw or
                                                    request.transaction_type == TransactionTypes.Card_To_Card_Out) :
            raise ValueError("You have reached your withdrawal limit.")

        if request.max_transaction >= 50000000 and (request.transaction_type == TransactionTypes.Withdraw or
                                                    request.transaction_type == TransactionTypes.Card_To_Card_Out) :
            raise ValueError("You have reached your withdrawal limit.")

        if self.next_handler:
            self.next_handler.handel(request)