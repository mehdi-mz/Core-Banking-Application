from BusinessLogic.validators.base_handler import BaseHandler


class ConfirmPasswordValidator(BaseHandler):
    def handel(self, request):
        if  not request.confirm_password.strip():
            raise ValueError("Confirm Password cannot be empty.")

        if request.password != request.confirm_password:
            raise ValueError("Password confirmation does not match.")

        if self.next_handler:
            self.next_handler.handel(request)

