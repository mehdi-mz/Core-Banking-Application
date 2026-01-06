from BusinessLogic.validators.base_handler import BaseHandler

class UsernameValidator(BaseHandler):


    def handel(self, request):
        if  not request.username.strip():
            raise ValueError("Username cannot be empty.")

        if  len(request.username.strip()) <= 5:
            raise ValueError("Username must be at least 5 characters ⚠")


        if self.next_handler:
            self.next_handler.handel(request)