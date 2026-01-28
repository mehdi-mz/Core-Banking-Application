from Common.Repositories.icustomer_repository import ICustomerRepository
from Common.DTOs.response import Response
from Common.entities.Enums.gender import Gender
import pymssql
from BusinessLogic.validators.create_customer.create_customer_request import CreateCustomerRequest
from BusinessLogic.validators.create_customer.birthdate_validator import BirthDateValidator
from BusinessLogic.validators.create_customer.name_validator import NameValidator
from BusinessLogic.validators.create_customer.nationalcode_validator import NationalCodeValidator
from BusinessLogic.validators.create_customer.phone_validator import PhoneNumberValidator



class CustomerBisinessLogic:
    def __init__(self,customer_repository : ICustomerRepository):
        self.customer_repository = customer_repository

    def get_customers(self, page_number=1, page_size=15, term=None):
        if term:
            try:
                customer = self.customer_repository.get_customers(page_number,page_size,term)
                return Response(True,"",customer)
            except Exception as e :
                print(f"Exception in get_customers(term): {e}")
                return Response(False,"Failed to fetch customers. ❌",None)

        else:
            try:
                customer = self.customer_repository.get_customers(page_number,page_size)
                return Response(True,"",customer)
            except Exception as e :
                print(f"Exception in get_customers: {e}")
                return Response(False,"Failed to fetch customers. ❌",None)

    def get_customer_by_id(self,customer_id):
        try:
            customer = self.customer_repository.get_customer_by_id(customer_id)
            return Response(True,"",customer)
        except Exception as e:
            print(f"Exception in update_customer: {e}")
            return Response(False, "Database error occurred. Please try again later.", None)


    def get_customer_by_national_code(self, national_code: str):
        if len(national_code.strip()) != 10 or not national_code.isdigit():
            return Response(False, "Please enter a valid national ID.", None)

        try:
            customer = self.customer_repository.get_customer_by_national_code(national_code)
            if customer:
                return Response(True,"", customer)
            else:
                return Response(False, "Customer not found!", None)
        except Exception as e:
            print(f"Exception in update_customer: {e}")
            return Response(False, "Database error occurred. Please try again later.", None)

    def create_customer(self, first_name, last_name, national_code, phone_number, email, birth_date, gender):

        request = CreateCustomerRequest(first_name,last_name,national_code,phone_number,birth_date,gender)

        name_validator = NameValidator()
        national_code_validator = NationalCodeValidator()
        phone_number_validator = PhoneNumberValidator()
        birthdate_validator = BirthDateValidator()

        name_validator.set_next(national_code_validator)
        national_code_validator.set_next(phone_number_validator)
        phone_number_validator.set_next(birthdate_validator)

        try:
            name_validator.handel(request)
        except ValueError as error :
            return Response(False,error.args[0],None)

        try:
            gender_value = Gender[gender].value
        except KeyError:
            return Response(False,"Invalid Gender value.",None)
        try:
            row= self.customer_repository.create_customer(first_name,last_name
                                                                ,national_code,phone_number,email,birth_date,gender_value)
            if row == 1 :
                return Response(True,"Customer was successfully created. ✅",None)
            else:
                return Response(False,"Failed to create customer. ❌",None)

        except pymssql.IntegrityError as e :
            error_msg = str(e)
            if "NationalCode unique" in error_msg:
                return Response(False,"This National Code is already registered ❌",None)
            elif "PhonNumber unique" in error_msg:
                return Response(False,"This phone number is already registered ❌",None)
            return Response(False,"Duplicate data error ❌",None)
        except Exception  as e:
            print(f"Exception in create_customer: {e}")
            return Response(False,"Database error occurred ❌. Please try again later.",None)

    def update_customer(self,customer_id,firstname,lastname,national_code,phon_number,email,birth_date,gender):

        request = CreateCustomerRequest(firstname,lastname,national_code,phon_number,birth_date,gender)

        name_validator = NameValidator()
        nationalcode_validator = NationalCodeValidator()
        phonenumber_validator = PhoneNumberValidator()
        birthdate_validator = BirthDateValidator()

        name_validator.set_next(nationalcode_validator)
        nationalcode_validator.set_next(phonenumber_validator)
        phonenumber_validator.set_next(birthdate_validator)

        try:
            name_validator.handel(request)
        except ValueError as error:
            return Response(False,error.args[0],None)

        try:
            gender_value = Gender[gender].value
        except KeyError:
            return Response(False,"Invalid Gender value.",None)

        try:
            row = self.customer_repository.update_customer(customer_id,firstname,lastname,national_code,phon_number
                                                     ,email,birth_date,gender_value)
            if row == 1 :
                return Response(True,"Information has been successfully updated. ✅",None)
            else:
                return Response(False,"Failed to update the information. ❌",None)
        except Exception as e :
            print(f"Exception in update_customer: {e}")
            return Response(False,"An error occurred while updating the information. ❌",None)

    def deactivated_customer(self,customer_id):
        try:
            rows = self.customer_repository.deactivated_customer(customer_id)
            if rows >= 1:
                return Response(True,"Customer deactivated successfully. ✅",None)
            else:
                return Response(False,"Customer not found or already deactivated. ❌",None)

        except Exception as e:
            print(f"Exception in deactivated_customer: {e}")
            return Response(False,"An internal error occurred while deactivating the customer. ❌",None)


    def blocked_customer(self,customer_id):
        try:
            rows = self.customer_repository.blocked_customer(customer_id)
            if rows >= 1:
                return Response(True, "Customer blocked successfully. ✅", None)
            else:
                return Response(False, "Customer not found or already blocked. ❌", None)

        except Exception as e:
            print(f"Exception in blocked_customer: {e}")
            return Response(False, "An internal error occurred while blocking the customer. ❌", None)

    def activated_customer(self,customer_id):
        try:
            rows = self.customer_repository.activated_customer(customer_id)
            if rows >= 1:
                return Response(True,"Customer Activated successfully. ✅",None)
            else:
                return Response(False,"Customer not found or already Activated. ❌",None)

        except Exception as e:
            print(f"Exception in activated_customer: {e}")
            return Response(False,"An internal error occurred while activating the customer. ❌",None)

    def get_customer_by_account_number(self,account_number):
        if  not account_number:
            return Response(False,"Account Number cannot be empty.",None)


        try:
            customer = self.customer_repository.get_customer_by_account_number(account_number)

            if customer:
                return Response(True,"",customer)
            else:
                return Response(False,"invalid account number. ❌",None)

        except Exception as e:
            print(f"Exception in get_customer_by_account_number: {e}")
            return Response(False, "Database error occurred ❌. Please try again later.", None)








