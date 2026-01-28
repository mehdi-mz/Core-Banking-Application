from dataclasses import dataclass

@dataclass
class ResetPasswordRequest:
    password : str
    confirm_password :str