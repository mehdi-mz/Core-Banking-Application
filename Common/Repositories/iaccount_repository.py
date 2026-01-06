from abc import ABC,abstractmethod


class IAccountRepository(ABC):
    @abstractmethod
    def get_account(self,page_number=1,page_size=15,term=None):
        pass

    @abstractmethod
    def get_account_by_id(self,account_number):
        pass

    @abstractmethod
    def create_account(self,customer_id,status_id,type_id):
        pass

    @abstractmethod
    def update_account(self,account_number,account_type,account_status):
        pass

    @abstractmethod
    def customer_accounts(self,customer_id):
        pass