from BusinessLogic.validators.base_handler import BaseHandler

class NameValidator(BaseHandler):


    def handel(self, request):
        if  not request.first_name.strip() or not isinstance(request.first_name,str):
            raise ValueError("First Name cannot be empty.")

        if not request.last_name.strip() or not isinstance(request.last_name, str):
            raise ValueError("Last Name cannot be empty.")


        if self.next_handler:
            self.next_handler.handel(request)