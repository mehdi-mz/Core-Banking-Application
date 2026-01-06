from Common.Repositories.iemployee_repository import IEmployeeRepository
from Common.entities.employee import Employee
import sqlite3


class SQLiteEmployeeRepository(IEmployeeRepository):
    def get_by_username_password(self, username:str, password:str):
        with sqlite3.connect("CoreBankingDB.db") as connetion:
            cursor = connetion.cursor()
            cursor.execute("""
                    select   id
                    ,        first_name
                    ,        last_name
                    ,        national_code 
                    ,        email
                    ,        username
                    ,        employee_status_id
                    ,        role_id
                    from employee
                    where username = ?
                    and   password = ?
                            """,(username,password))
            data = cursor.fetchone()
            if data is None:
                return None
            employee = Employee(*data)
            return employee



    def reset_password(self,new_password,username):
        with sqlite3.connect("CoreBankingDB.db") as connetion:
            cursor = connetion.cursor()
            cursor.execute("""
                            update employee 
                            set    password = ?
                            where  username = ?
                                                        """,(new_password,username))

            connetion.commit()

            return cursor.rowcount



    def update_profile(self,id_employee,new_firstname,new_lastname,new_username,new_nationalcode,new_emil):
        with sqlite3.connect("CoreBankingDB.db") as connetion:
            cursor = connetion.cursor()
            cursor.execute("""
                            update employee
                            set   first_name = ?
                            ,     last_name  = ?
                            ,     national_code = ? 
                            ,     email = ? 
                            ,     username = ?
                            where  id = ? 
                            """,(new_firstname,new_lastname,new_nationalcode,new_emil,new_username,id_employee))
            connetion.commit()

            return cursor.rowcount



