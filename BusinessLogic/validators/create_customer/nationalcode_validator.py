from BusinessLogic.validators.base_handler import BaseHandler

class NationalCodeValidator(BaseHandler):

    def handel(self, request):
        if  not request.national_code.strip():
            raise ValueError("Please enter a valid national code ⚠️.")

        if len(request.national_code.strip())!= 10:
            raise ValueError("National Code value is out of valid range.")

        if   not request.national_code.isdigit():
            raise  ValueError("Invalid National Code value please enter integer type.")

        if self.next_handler:
            self.next_handler.handel(request)