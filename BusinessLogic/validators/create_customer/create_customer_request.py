from dataclasses import dataclass

@dataclass
class CreateCustomerRequest:
    first_name : str
    last_name : str
    national_code : str
    phone_number : str
    email : str
    birth_date : str
    gender : str