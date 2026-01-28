from BusinessLogic.validators.base_handler import BaseHandler


class MaxTransactionValidator(BaseHandler):
    def handel(self, request):
        if request.max_transaction >= 50000000 and (request.transaction_type == "Withdraw" or
                                                    request.transaction_type == "Card_To_Card_Out") :
            raise ValueError("You have reached your withdrawal limit.")

        if self.next_handler:
            self.next_handler.handel(request)