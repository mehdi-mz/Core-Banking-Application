from Common.entities.Enums.employee_status import EmployeeStatus
from Common.entities.Enums.employee_role import EmployeeRole

class Employee:
    def __init__(self,id,firstname,lastname,national_code,email,username,status_id,role_id,regester_date,accept_date,status_changed_date):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.national_code = national_code
        self.email = email
        self.username = username
        self.status_id = EmployeeStatus(status_id)
        self.role_id = EmployeeRole(role_id)
        self.regester_date =regester_date
        self.accept_date = accept_date
        self.status_changed_date = status_changed_date


    def full_name(self):
        return f"{self.firstname} {self.lastname}"

    @classmethod
    def create_with_dict(cls, dic_data):
        return cls(
            dic_data.get("Id"),
            dic_data.get("First_Name"),
            dic_data.get("Last_Name"),
            dic_data.get("NationalCode"),
            dic_data.get("Email"),
            dic_data.get("UserName"),
            dic_data.get("EmployeeStatus"),
            dic_data.get("Role_id"),
            dic_data.get("regester_date"),
            dic_data.get("accept_date"),
            dic_data.get("status_changed_date"))
