from BusinessLogic.validators.base_handler import BaseHandler


class BirthDateValidator(BaseHandler):

    def handel(self,request):
        if not request.birth_date.strip() or request.birth_date == "1900-01-01":
            raise ValueError("Birth Date cannot be empty.")

        if len(request.birth_date) != 10 :
            raise ValueError("The entered date is invalid ⚠️")


        if self.next_handler:
            self.next_handler.handel(request)