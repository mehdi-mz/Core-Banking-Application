from enum import Enum

class TransactionTypes(Enum):
    Deposit = 1
    Withdraw = 2
    Card_To_Card_Out = 3
    Card_To_Card_In = 4