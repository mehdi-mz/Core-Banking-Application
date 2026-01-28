from abc import ABC,abstractmethod


class ITransactionRepository(ABC):

    @abstractmethod
    def get_transactions(self,account_number:int,page_number=1,page_size=15):
        pass

    @abstractmethod
    def get_all_transactions(self,account_number:int):
        pass


    @abstractmethod
    def insert_transaction(self,new_transaction):
        pass

    @abstractmethod
    def sum_balance(self,account_number):
        pass


    @abstractmethod
    def get_daily_transactions(self,account_number):
        pass

    @abstractmethod
    def card_to_card(self,new_transaction,old_balance_card):
        pass