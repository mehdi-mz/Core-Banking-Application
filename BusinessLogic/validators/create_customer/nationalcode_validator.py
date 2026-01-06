from BusinessLogic.validators.base_handler import BaseHandler

class NationalCodeValidator(BaseHandler):

    def handel(self, request):
        if  (not request.national_code.strip() or len(request.national_code.strip())!= 10
                or  not request.national_code.isdigit()):
            raise ValueError("Please enter a valid national code ⚠️.")

        if self.next_handler:
            self.next_handler.handel(request)