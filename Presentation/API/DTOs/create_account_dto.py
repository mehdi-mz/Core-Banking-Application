from pydantic import BaseModel , Field

class CreateAccountDTO(BaseModel):
    national_code:str = Field(default="")
    account_status_id : int = Field(ge=1,le=3,default=1,description="1=>Active  2=>Deactivate  3=>Block")
    account_type_id :int = Field(ge=1,le=3,default=1,description="1=>Current Account   2=>Currency Account   3=>Gharzol Hasaneh")

