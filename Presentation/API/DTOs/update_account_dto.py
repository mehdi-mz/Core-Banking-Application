from pydantic import BaseModel ,Field
from typing import Optional

class UpdateAccountDTO(BaseModel):
    account_status_id:Optional[int]=Field(default=None)
    account_type_id:Optional[int]=Field(default=None)