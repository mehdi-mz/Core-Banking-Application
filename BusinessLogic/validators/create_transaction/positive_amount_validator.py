from BusinessLogic.validators.base_handler import BaseHandler


class PositiveAmountValidator(BaseHandler):
    def handel(self, request):
        if  not request.transaction_amount :
            raise ValueError("Amount cannot be empty.")

        if not request.transaction_type:
            raise ValueError("Transaction Type cannot be empty.")

        if request.transaction_amount < 10000:
            raise ValueError("Invalid amount for new transaction.")

        if self.next_handler:
            self.next_handler.handel(request)