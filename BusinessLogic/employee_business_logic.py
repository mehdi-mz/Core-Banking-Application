from Common.DTOs.response import Response
from Common.Repositories.iemployee_repository import IEmployeeRepository
from hashlib import md5
import pymssql
from Common.entities.Enums.employee_status import EmployeeStatus
from Common.entities.Enums.employee_role import EmployeeRole

from BusinessLogic.validators.create_employee.create_employee_request import CreateEmployeeRequest
from BusinessLogic.validators.create_customer.name_validator import NameValidator
from BusinessLogic.validators.create_customer.nationalcode_validator import NationalCodeValidator
from BusinessLogic.validators.create_employee.email_validator import EmailValidator
from BusinessLogic.validators.create_employee.username_validator import UsernameValidator
from BusinessLogic.validators.login_employee.password_validator import PasswordValidator
from BusinessLogic.validators.login_employee.login_employee_request import LoginEmployeeRequest
from BusinessLogic.validators.reset_password.confirm_password_validator import ConfirmPasswordValidator
from BusinessLogic.validators.reset_password.reset_passwoed_request import ResetPasswordRequest

class EmployeeBusinessLogic:
    def __init__(self,employee_repository:IEmployeeRepository):
        self.employee_repository=employee_repository

    def login(self,username:str,password:str,entry_captcha,data_captcha):
        request = LoginEmployeeRequest(username,password)

        username_validator = UsernameValidator()
        password_validator = PasswordValidator()
        username_validator.set_next(password_validator)
        try:
            username_validator.handel(request)
        except ValueError as error :
            return Response(False,error.args[0],None)


        if entry_captcha != data_captcha:
            return Response(False,"Please enter the captcha correctly.",None)

        pssword_hash = md5(password.encode()).hexdigest()
        employee = self.employee_repository.get_by_username_password(username,pssword_hash)

        if employee:
            if employee.status_id != EmployeeStatus.Active:
                return Response(False,"invalid usernamaeee or password !",None)
            else:
                return Response(True,f"welcom {employee.full_name()}",employee)
        else:
            return Response(False,"invalid usernamae or password !",None)



    def reset_password(self,employee_id,new_password,confirm_password,entry_captcha,data_captcha):
        request = ResetPasswordRequest(new_password,confirm_password)

        password_validator = PasswordValidator()
        confirm_password_validatoe = ConfirmPasswordValidator()
        password_validator.set_next(confirm_password_validatoe)
        try:
            password_validator.handel(request)
        except ValueError as error :
            return Response(False,error.args[0],None)

        if entry_captcha != data_captcha:
            return Response(False, "Please enter the captcha correctly.", None)

        new_password_hash = md5(new_password.encode()).hexdigest()
        set_password = self.employee_repository.reset_password(new_password_hash,employee_id)

        if set_password == 1 :
            return Response(True,"Your password has been successfully reset.",None)
        else:
            return Response(False,"Your password reset was not successful. Please try again.",None)




    def update_profile(self,employee_id,new_firstname,new_lastname,new_username,new_national_code,
                       new_email,role_id,new_status=None):

        request = CreateEmployeeRequest(new_firstname,new_lastname,new_username,new_national_code,new_email)

        name_validator = NameValidator()
        username_validator = UsernameValidator()
        national_code_validator = NationalCodeValidator()
        email_validator = EmailValidator()

        name_validator.set_next(username_validator)
        username_validator.set_next(national_code_validator)
        national_code_validator.set_next(email_validator)

        try:
            name_validator.handel(request)
        except ValueError as error :
            return Response(False,error.args[0],None)

        try:
            role_value = EmployeeRole[role_id].value
        except KeyError:
            return Response(False, "Invalid Employee Role value.", None)

        try:
            if new_status:
                status_value = EmployeeStatus[new_status].value
                update_data_employee=self.employee_repository.update_profile(employee_id,new_firstname,new_lastname,
                                                                         new_username,new_national_code,new_email,role_value,status_value)
            else:
                update_data_employee = self.employee_repository.update_profile(employee_id, new_firstname, new_lastname,
                                                                               new_username, new_national_code,
                                                                               new_email,role_value)
            if update_data_employee == 1 :
                return Response(True,"Information has been successfully updated. ✅",None)
            else:
                return Response(False,"Your profile update encountered an error. Please try again later.",None)
        except Exception as e:
            print(f"Exception in update_profile: {e}")
            return Response(False, "An error occurred while updating your profile. ❌", None)

    def employee_management(self,page_number=1,page_size=15,term =None):
        if term:
            try:
                employee_list = self.employee_repository.get_employee(page_number, page_size,term)
                return Response(True,"", employee_list)
            except Exception as e:
                print(f"Exception in employee_management(term): {e}")
                return Response(False, "Load Employee List failed!", None)
        else:
            try:
                 employee_list = self.employee_repository.get_employee(page_number,page_size)
                 return Response(True,"",employee_list)
            except Exception as e:
                print(f"Exception in employee_management: {e}")
                return Response(False,"Load Employee List failed!",None)
            # employee_list = self.employee_repository.get_employee(page_number, page_size)

    def request_employee(self,page_number=1,page_size=15,term = None):
        if term:
            try:
                request = self.employee_repository.request_employee(page_number, page_size,term)
                return Response(True,"", request)
            except Exception as e:
                print(f"Exception in request_employee(term): {e}")
                return Response(False, "Load Employee Request  List failed!", None)
        else:
            try:
                request  = self.employee_repository.request_employee(page_number, page_size)
                return Response(True,"", request)
            except Exception as e:
                print(f"Exception in request_employee: {e}")
                return Response(False, "Load Employee Request  List failed!", None)
            # request = self.employee_repository.get_employee(page_number, page_size)

    def register_employee(self,first_name, last_name, national_code, email, username,password ,confirm_password):

        request = CreateEmployeeRequest(first_name, last_name, username, national_code, email)

        name_validator = NameValidator()
        username_validator = UsernameValidator()
        national_code_validator = NationalCodeValidator()
        email_validator = EmailValidator()

        name_validator.set_next(username_validator)
        username_validator.set_next(national_code_validator)
        national_code_validator.set_next(email_validator)

        try:
            name_validator.handel(request)
        except ValueError as error:
            return Response(False, error.args[0], None)


        if password != confirm_password:
            return Response(False,"Passwords do not match.",None)


        password_hash=md5(password.encode()).hexdigest()
        try:
            row = self.employee_repository.register_employee(first_name,last_name,national_code,email,username,password_hash)

            if row == 1:
                return Response(True, "Your registration was successful.✅  Please wait for account activation.", None)
            else:
                return Response(False, "Registration failed. Please try again.", None)

        except pymssql.IntegrityError as e :
            error_msg = str(e)

            if "UQ_Employee_UserName" in error_msg:
                return Response(False, "Username already exists.", None)

            elif "UQ_Employee_nationalcode" in error_msg:
                return Response(False, "National code already exists.", None)

            else:
                return Response(False, "Duplicate data detected.", None)


        except pymssql.OperationalError:
            return Response(False, "Database connection error. Please try again later.", None)

        except Exception as e:
            print(f"Exception in register_employee: {e}")
            return Response(False, "An unexpected error occurred.", None)

    def get_employee_by_id(self,employee_id):
        try:
            employee = self.employee_repository.get_employee_by_id_(employee_id)
            return Response(True,"",employee)
        except Exception as e:
            print(f"Exception in get_employee_by_id: {e}")
            Response(False," data failed",None)

    def accept_employee(self,employee_id):
        try:
            accept_employee = self.employee_repository.accept_employee(employee_id)
            if accept_employee == 1:
                return Response(True,"The employee has been accepted successfully.",None)
            else:
                return Response(False, "Employee not found or already accepted.", None)
        except Exception as e :
            print(f"Exception in accept_employee: {e}")
            return Response(False,"A database error occurred while accepting the employee.",None)

    def reject_employee(self,employee_id):
        try:
            reject_employee = self.employee_repository.reject_employee(employee_id)
            if reject_employee == 1:
                return Response(True,"The employee has been rejected successfully.",None)
            else:
                return Response(False, "Employee not found or already rejected.", None)
        except Exception as e :
            print(f"Exception in reject_employee: {e}")
            return Response(False,"A database error occurred while rejecting the employee.",None)

    def get_reject_employee(self, page_number=1, page_size=15, term=None):
        if term:
            try:
                rejected = self.employee_repository.get_reject_employees(page_number, page_size, term)
                return Response(True,"", rejected)
            except Exception as e:
                print(f"Exception in request_employee(term): {e}")
                return Response(False, "Load Employee Request  List failed!", None)
        else:
            try:
                rejected = self.employee_repository.get_reject_employees(page_number, page_size)
                return Response(True,"", rejected)
            except Exception as e:
                print(f"Exception in request_employee: {e}")
                return Response(False, "Load Employee Request  List failed!", None)

    def get_deactivated_employee(self, page_number=1, page_size=15, term=None):
        if term:
            try:
                deactivated = self.employee_repository.get_deactivated_employee(page_number, page_size, term)
                return Response(True, "", deactivated)
            except Exception as e:
                print(f"Exception in request_employee(term): {e}")
                return Response(False, "Load Employee Request  List failed!", None)
        else:
            try:
                deactivated = self.employee_repository.get_deactivated_employee(page_number, page_size)
                return Response(True, "", deactivated)
            except Exception as e:
                print(f"Exception in request_employee: {e}")
                return Response(False, "Load Employee Request  List failed!", None)

