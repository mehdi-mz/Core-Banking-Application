from BusinessLogic.validators.base_handler import BaseHandler

class EmailValidator(BaseHandler):


    def handel(self, request):
        if  not request.email.strip() or not isinstance(request.email,str):
            raise ValueError("Email cannot be empty.")

        if not request.email.endswith("@gmail.com"):
            raise ValueError("The email must be a valid Gmail address ⚠️")


        if self.next_handler:
            self.next_handler.handel(request)