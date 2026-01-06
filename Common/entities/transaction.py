from Common.entities.Enums.transaction_types import TransactionTypes



class Transaction:
    def __init__(self,id,account_number,old_balance,amount,transaction_type,user_name,transaction_time):
        self.id = id
        self.account_number = account_number
        self.old_balance = old_balance
        self.amount = amount
        self.transaction_type = TransactionTypes(transaction_type)
        self.user_name = user_name
        self.transaction_time = transaction_time

    @classmethod
    def create_with_dict(cls,dic_data):
        return cls(
            dic_data.get("id"),
            dic_data.get("Account_Number"),
            dic_data.get("Old_Balance"),
            dic_data.get("Amount"),
            dic_data.get("TransactionType"),
            dic_data.get("UserName"),
            dic_data.get("TransactionTime"))

