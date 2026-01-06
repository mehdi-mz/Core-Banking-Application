from BusinessLogic.validators.base_handler import BaseHandler


class PhoneNumberValidator(BaseHandler):

    def handel(self, request):
        if (not request.phone_number.strip() or
                len(request.phone_number.strip()) != 11 or not request.phone_number.isdigit()):
            raise ValueError("The Phone Number entered is invalid ⚠️.")

        if self.next_handler:
            self.next_handler.handel(request)