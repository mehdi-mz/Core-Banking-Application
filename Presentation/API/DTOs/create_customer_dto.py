from pydantic import BaseModel , Field

class CreateCustomerDTO(BaseModel):
    firstname : str = Field(default="")
    lastname : str = Field(default="")
    national_code : str = Field(default="")
    phon_number : str = Field(default="")
    email : str = Field(default="")
    birth_date : str = Field(default="1900-01-01")
    gender_id :int =Field(ge=0,le=1,default=0, description="0 => Male -1 => Female")