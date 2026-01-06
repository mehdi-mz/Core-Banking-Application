from abc import ABC ,abstractmethod


class ICustomerRepository(ABC):


    @abstractmethod
    def get_customers(self, page_number=1, page_size=15,term=None):
        pass

    @abstractmethod
    def get_customer_by_id(self,customer_id):
        pass

    @abstractmethod
    def get_customer_by_national_code(self,national_code):
        pass

    @abstractmethod
    def create_customer(self,first_name,last_name,national_code,phon_number,email,birth_date,gender):
        pass

    @abstractmethod
    def update_customer(self,customer_id,firstname,lastname,national_code,phon_number,email,birth_date,gender):
        pass

    @abstractmethod
    def blocked_customer(self,customer_id):
        pass

    @abstractmethod
    def deactivated_customer(self, customer_id):
        pass