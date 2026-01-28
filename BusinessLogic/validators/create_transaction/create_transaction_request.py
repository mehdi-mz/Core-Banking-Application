from dataclasses import dataclass
from Common.entities.account import Account
from Common.entities.Enums.transaction_types import TransactionTypes

@dataclass
class CreateTransactionRequest:
    account : Account
    transaction_amount : float
    balance : float
    transaction_type : TransactionTypes
    max_transaction :float
    card : Account = None