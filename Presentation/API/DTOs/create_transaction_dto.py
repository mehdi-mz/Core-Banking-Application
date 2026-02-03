from pydantic import BaseModel ,Field
from typing import Optional


class CreateTransactionDTO(BaseModel):
    amount : float = Field(ge=1000)
    transaction_type_id :int = Field(ge=1,le=3,default=1,description="1=>Deposit -2=>Withdraw -3=>Card To Card")
    account_number : int =Field(ge=1000)
    card : Optional[int] = Field(default=None)
