from dataclasses import dataclass

@dataclass
class ResetPasswoedRequest:
    password : str
    confirm_password :str