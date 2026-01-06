from BusinessLogic.validators.base_handler import BaseHandler

class PasswordValidator(BaseHandler):

    def handel(self,request):
        if not request.password.strip():
            raise ValueError("Password cannot be empty.")

        if len(request.password) < 6:
            raise ValueError("Password must be at least 6 characters ⚠️")



        if self.next_handler:
            self.next_handler.handel(request)