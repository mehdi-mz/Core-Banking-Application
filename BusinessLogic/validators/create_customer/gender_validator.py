from BusinessLogic.validators.base_handler import BaseHandler
from Common.entities.Enums.gender import Gender

class GenderValidator(BaseHandler):

    def handel(self, request):
        if not isinstance(request.gender,Gender):
            raise ValueError("Invalid Gender type.")



            # raise ValueError("Gender cannot be empty.")

        if self.next_handler:
            self.next_handler.handel(request)