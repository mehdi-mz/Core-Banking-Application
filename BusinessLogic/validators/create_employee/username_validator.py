from BusinessLogic.validators.base_handler import BaseHandler

class UsernameValidator(BaseHandler):


    def handel(self, request):
        if  not request.username.strip():
            raise ValueError("Username cannot be empty.")

        if len(request.username) > 50 or len(request.username.strip()) <= 5 :
            raise ValueError("Username value is out of valid range (5 <= Username => 50)")


        if self.next_handler:
            self.next_handler.handel(request)