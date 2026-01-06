from dataclasses import dataclass


@dataclass
class LoginEmployeeRequest:
    username : str
    password : str