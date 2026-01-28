from BusinessLogic.validators.base_handler import BaseHandler


class PhoneNumberValidator(BaseHandler):

    def handel(self, request):
        if not request.phone_number.strip():
            raise ValueError("Phone Number cannot be empty.")

        if len(request.phone_number.strip()) != 11:
            raise ValueError("Phone Number value is out of valid range.")

        if   not request.phone_number.isdigit():
            raise ValueError("Invalid Phone Number value please enter integer type⚠️. ")

        if self.next_handler:
            self.next_handler.handel(request)