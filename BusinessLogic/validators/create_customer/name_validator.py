from BusinessLogic.validators.base_handler import BaseHandler

class NameValidator(BaseHandler):


    def handel(self, request):
        if  not request.first_name.strip() :
            raise ValueError("First Name cannot be empty.")

        if  not isinstance(request.first_name,str):
            raise ValueError("Invalid value please enter string type.")

        if len(request.first_name) > 50:
            raise ValueError("First name value is out of valid range.")


        if not request.last_name.strip():
            raise ValueError("Last Name cannot be empty.")

        if not isinstance(request.last_name, str):
            raise ValueError("Invalid value please enter string type.")

        if len(request.last_name) > 50:
            raise ValueError("Last name value is out of valid range.")


        if self.next_handler:
            self.next_handler.handel(request)