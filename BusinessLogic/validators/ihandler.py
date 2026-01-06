from abc import ABC,abstractmethod

class IHandler(ABC):
    @abstractmethod
    def set_next(self,next_handler):
        pass

    @abstractmethod
    def handel(self,request):
        pass