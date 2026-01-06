import pymssql
from Common.Repositories.iemployee_repository import IEmployeeRepository
from Common.entities.employee import Employee

class SQLServerEmployeeRepository(IEmployeeRepository):

    def creat_connection(self):
        connection=pymssql.connect(host=".",
        database="Bank Management Application")
        return connection

    def get_by_username_password(self,username,password):
        with self.creat_connection() as connection:
            cursor=connection.cursor(as_dict=True)
            cursor.execute("""
                    select   Id
                            ,First_Name 
                            ,Last_Name      
                            ,NationalCode
                            ,Email
                            ,UserName
                            ,EmployeeStatus
                            ,Role_id
                            ,regester_date
                            ,accept_date
                            ,status_changed_date
                    from staff.Employee
                    where username = %s
                    and   password = %s
                            """,(username,password))
            data=cursor.fetchone()
            if data is None:
                return None
            employee=Employee.create_with_dict(data)
            return employee


    def reset_password(self,new_password,employee_id):
        with self.creat_connection() as connection:
            cursor = connection.cursor(as_dict=True)
            cursor.execute("""
                            update staff.employee 
                            set    password = %s
                            where  id = %d
                                                        """,(new_password,employee_id))

            connection.commit()

            return cursor.rowcount



    def update_profile(self,employee_id,new_firstname,new_lastname,new_username,new_nationalcode,new_emil,new_status=None):
        with self.creat_connection() as connection:
            cursor = connection.cursor()
            if new_status :
                cursor.execute("""
                                update staff.Employee
                                set   first_name = %s
                                ,     last_name  = %s
                                ,     nationalcode = %s 
                                ,     email = %s
                                ,     username = %s
                                ,     EmployeeStatus = %d
                                ,     status_changed_date = getdate()
                                where  id = %d
                                """,(new_firstname,new_lastname,new_nationalcode,new_emil
                                                                        ,new_username,new_status,employee_id))
                connection.commit()
            else:
                cursor.execute("""
                                               update staff.Employee
                                               set   first_name = %s
                                               ,     last_name  = %s
                                               ,     nationalcode = %s 
                                               ,     email = %s
                                               ,     username = %s
                                               where  id = %d
                                               """,
                               (new_firstname, new_lastname, new_nationalcode, new_emil, new_username, employee_id))
                connection.commit()

            return cursor.rowcount

    def get_employee(self, page_number=1, page_size=15,term=None):
        employee_list = []
        skip_rows = (page_number-1)*page_size
        with self.creat_connection() as connection :
            cursor = connection.cursor(as_dict=True)
            if term:
                query = """select  Id
                                 ,First_Name
                                 ,Last_Name
                                 ,NationalCode
                                 ,Email
                                 ,UserName
                                 ,EmployeeStatus
                                 ,Role_id
                                 ,regester_date
                                 ,accept_date
                                ,status_changed_date
                         from staff.Employee
                         where EmployeeStatus = 2
                         and  ( First_Name like %s
                         or    Last_Name  like %s
                         or    NationalCode like %s
                         or    UserName  like %s)
                         order by regester_date desc
                         offset %d rows 
                         fetch next %d  rows only"""
                value = f'%{term}%'
                cursor.execute(query, (value, value, value, value, skip_rows, page_size))
                data = cursor.fetchall()
                for row in data:
                    employee = Employee.create_with_dict(row)
                    employee_list.append(employee)

            else:
                cursor.execute("""
                            select  Id
                                    ,First_Name
                                    ,Last_Name
                                    ,NationalCode
                                    ,Email
                                    ,UserName
                                    ,EmployeeStatus
                                    ,Role_id
                                    ,regester_date
                                    ,accept_date
                                    ,status_changed_date
                            from staff.Employee
                            where EmployeeStatus = 2
                            order by accept_date desc
                            offset %d rows 
                            fetch next %d  rows only
                                     """,(skip_rows,page_size))
                data =cursor.fetchall()
                for row in data:
                    employee = Employee.create_with_dict(row)
                    employee_list.append(employee)
        return employee_list

    def request_employee(self,page_number=1,page_size=15,term=None):
        request_list = []
        skip_rows = (page_number-1)*page_size
        with self.creat_connection() as connection :
            cursor = connection.cursor(as_dict=True)
            if term:
                query = """select  Id
                                    ,First_Name
                                    ,Last_Name
                                    ,NationalCode
                                    ,Email
                                    ,UserName
                                    ,EmployeeStatus
                                    ,Role_id
                                    ,regester_date
                                    ,accept_date
                                    ,status_changed_date
                            from staff.Employee
                            where EmployeeStatus = 1
                            and  ( First_Name like %s
                            or    Last_Name  like %s
                            or    NationalCode like %s
                            or    UserName  like %s)
                            order by regester_date desc
                            offset %d rows 
                            fetch next %d  rows only"""
                value = f'%{term}%'
                cursor.execute(query,(value,value,value,value,skip_rows,page_size))
                data = cursor.fetchall()
                for row in data:
                    request = Employee.create_with_dict(row)
                    request_list.append(request)
            else:
                cursor.execute("""
                        select  Id
                                ,First_Name
                                ,Last_Name
                                ,NationalCode
                                ,Email
                                ,UserName
                                ,EmployeeStatus
                                ,Role_id
                                ,regester_date
                                ,accept_date
                                 ,status_changed_date
                        from staff.Employee
                        where EmployeeStatus = 1
                        order by regester_date desc
                        offset %d rows 
                        fetch next %d  rows only
                                 """,(skip_rows,page_size))
                data = cursor.fetchall()
                for row in data:
                    request = Employee.create_with_dict(row)
                    request_list.append(request)
        return request_list

    def register_employee(self, first_name, last_name, national_code, email, username,password):
        with self.creat_connection() as connection :
            cursor = connection.cursor()
            cursor.execute("""
                        insert staff.Employee(First_Name,Last_Name,NationalCode,Email,UserName,Password,EmployeeStatus,Role_id)
                        values(
                                %s,%s,%s,%s,%s,%s,%d,%d)
                            """,(first_name,last_name,national_code,email,username,password,1,2))
            connection.commit()
            return cursor.rowcount

    def get_employee_by_id_(self, employee_id):
        with self.creat_connection() as connection :
            cursor = connection.cursor(as_dict=True)
            cursor.execute("""
                            select id,
                                    First_Name,
                                    Last_Name,
                                    NationalCode,
                                    Email,
                                    UserName,
                                    EmployeeStatus,
                                    Role_id,
                                    regester_date
                                    ,accept_date
                                    ,status_changed_date
                            from staff.Employee
                            where Id = %d

                        """,employee_id)
            data = cursor.fetchone()
            employee = Employee.create_with_dict(data)
        return employee

    def accept_employee(self, employee_id):
        with self.creat_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                            update staff.Employee
                            set   EmployeeStatus = %d
                            ,     accept_date = GETDATE()
                            where  id = %d
                            """,  (2,employee_id))
            connection.commit()

            return cursor.rowcount



    def reject_employee(self, employee_id):
        with self.creat_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                            update staff.Employee
                            set   EmployeeStatus = %d
                            where  id = %d
                            """, (4, employee_id))
            connection.commit()

            return cursor.rowcount

    def get_reject_employees(self,page_number=1,page_size=15,term=None):
        request_list = []
        skip_rows = (page_number-1)*page_size
        with self.creat_connection() as connection :
            cursor = connection.cursor(as_dict=True)
            if term:
                query = """select  Id
                                    ,First_Name
                                    ,Last_Name
                                    ,NationalCode
                                    ,Email
                                    ,UserName
                                    ,EmployeeStatus
                                    ,Role_id
                                    ,regester_date
                                    ,accept_date
                                    ,status_changed_date
                            from staff.Employee
                            where EmployeeStatus = 4
                            and  ( First_Name like %s
                            or    Last_Name  like %s
                            or    NationalCode like %s
                            or    UserName  like %s)
                            order by regester_date desc
                            offset %d rows 
                            fetch next %d  rows only"""
                value = f'%{term}%'
                cursor.execute(query,(value,value,value,value,skip_rows,page_size))
                data = cursor.fetchall()
                for row in data:
                    request = Employee.create_with_dict(row)
                    request_list.append(request)
            else:
                cursor.execute("""
                        select  Id
                                ,First_Name
                                ,Last_Name
                                ,NationalCode
                                ,Email
                                ,UserName
                                ,EmployeeStatus
                                ,Role_id
                                ,regester_date
                                ,accept_date
                                ,status_changed_date
                        from staff.Employee
                        where EmployeeStatus = 4
                        order by regester_date desc
                        offset %d rows 
                        fetch next %d  rows only
                                 """,(skip_rows,page_size))
                data = cursor.fetchall()
                for row in data:
                    request = Employee.create_with_dict(row)
                    request_list.append(request)
        return request_list


    def get_deactivated_employee(self,page_number=1,page_size=15,term=None):
        request_list = []
        skip_rows = (page_number-1)*page_size
        with self.creat_connection() as connection :
            cursor = connection.cursor(as_dict=True)
            if term:
                query = """select  Id
                                    ,First_Name
                                    ,Last_Name
                                    ,NationalCode
                                    ,Email
                                    ,UserName
                                    ,EmployeeStatus
                                    ,Role_id
                                    ,regester_date
                                    ,accept_date
                                    ,status_changed_date
                            from staff.Employee
                            where EmployeeStatus = 3
                            and  ( First_Name like %s
                            or    Last_Name  like %s
                            or    NationalCode like %s
                            or    UserName  like %s)
                            order by regester_date desc
                            offset %d rows 
                            fetch next %d  rows only"""
                value = f'%{term}%'
                cursor.execute(query,(value,value,value,value,skip_rows,page_size))
                data = cursor.fetchall()
                for row in data:
                    request = Employee.create_with_dict(row)
                    request_list.append(request)
            else:
                cursor.execute("""
                        select  Id
                                ,First_Name
                                ,Last_Name
                                ,NationalCode
                                ,Email
                                ,UserName
                                ,EmployeeStatus
                                ,Role_id
                                ,regester_date
                                ,accept_date
                                ,status_changed_date
                        from staff.Employee
                        where EmployeeStatus = 3
                        order by regester_date desc
                        offset %d rows 
                        fetch next %d  rows only
                                 """,(skip_rows,page_size))
                data = cursor.fetchall()
                for row in data:
                    request = Employee.create_with_dict(row)
                    request_list.append(request)
        return request_list










