from BusinessLogic.validators.ihandler import IHandler

class BaseHandler(IHandler):
    def __init__(self):
        self.next_handler = None

    def set_next(self, next_handler):
        self.next_handler = next_handler

    def handel(self, request):
        pass