from abc import ABC,abstractmethod
class IEmployeeRepository(ABC):
    @abstractmethod
    def get_by_username_password(self,username,password):
        pass

    @abstractmethod
    def reset_password(self,new_password,username):
        pass

    @abstractmethod
    def update_profile(self, id_employee, new_firstname, new_lastname, new_username, new_nationalcode, new_emil,new_status=None):
        pass


    @abstractmethod
    def get_employee(self,page_number=1,page_size=15,term=None):
        pass

    @abstractmethod
    def request_employee(self,page_number=1,page_size=15,term=None):
        pass

    @abstractmethod
    def register_employee(self,first_name , last_name ,national_code , email , username,password):
        pass


    @abstractmethod
    def get_employee_by_id_(self,id):
        pass


    @abstractmethod
    def accept_employee(self,employee_id):
        pass

    @abstractmethod
    def reject_employee(self,employee_id):
        pass

    @abstractmethod
    def get_reject_employees(self, page_number=1, page_size=15, term=None):
        pass

    @abstractmethod
    def get_deactivated_employee(self, page_number=1, page_size=15, term=None):
        pass



