from Common.entities.customer import Customer
from Common.entities.Enums.account_status import AccountStatus
from Common.entities.Enums.account_types import AccountTypes


class Account:
    def __init__(self,account_number,customer:Customer,account_status,created_date,account_type):
        self.account_number = account_number
        self.customer = customer
        self.account_status = AccountStatus(account_status)
        self.created_date = created_date
        self.account_type = AccountTypes(account_type)

    @classmethod
    def create_with_dict(cls,data_dic,customer):
        return cls(
            data_dic.get("Account_Number"),
            customer,
            data_dic.get("StatusId"),
            data_dic.get("Created_Date"),
            data_dic.get("AccountTypeId"),
        )
