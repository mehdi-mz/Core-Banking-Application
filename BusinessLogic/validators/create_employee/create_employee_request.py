from dataclasses import dataclass

@dataclass
class CreateEmployeeRequest:
    first_name : str
    last_name : str
    username : str
    national_code : str
    email : str
