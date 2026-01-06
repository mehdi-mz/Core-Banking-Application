from Common.Repositories.icustomer_repository import ICustomerRepository
from Common.entities.customer import Customer
import pymssql

class SqlServerCustomerRepository(ICustomerRepository):

    def creat_connection(self):
        connection = pymssql.connect(host=".", database="Bank Management Application")
        return connection

    def get_customers(self, page_number=1, page_size=15, term=None):
        customer_list=[]
        skip_rows = (page_number-1)*page_size
        with self.creat_connection() as connection :
            cursor = connection.cursor(as_dict=True)
            if term:
                query = """select   id   as customer_id
                                    ,First_Name,Last_Name
                                    ,NationalCode,PhonNumber
                                    ,Email,BirthDate,Gender
                            from Customer 
                            where First_Name like %s
                            or    Last_Name  like %s
                            or    NationalCode like %s
                            order by id desc
                            offset %d rows 
                            fetch next %d  rows only """

                value = f'%{term}%'
                cursor.execute(query,(value,value,value,skip_rows,page_size))
                data = cursor.fetchall()
                for row in data:
                    customer = Customer.create_with_dict(row)
                    customer_list.append(customer)
            else:
                cursor.execute("""select     id   as customer_id
                                        ,First_Name,Last_Name
                                        ,NationalCode,PhonNumber
                                        ,Email,BirthDate,Gender
                                 from Customer
                                 order by id desc 
                                 offset %d rows 
                                 fetch next %d  rows only
                                """,(skip_rows,page_size))
                data = cursor.fetchall()
                for row in data:
                    customer = Customer.create_with_dict(row)
                    customer_list.append(customer)
        return customer_list


    def get_customer_by_id(self, customer_id):
        with self.creat_connection() as connection:
            cursor = connection.cursor(as_dict=True)
            cursor.execute("""select    Id  as  customer_id
                                                  ,First_Name,Last_Name
                                                  ,NationalCode,PhonNumber
                                                  ,Email,BirthDate,Gender
                                          from Customer
                                          where id = %d""", (customer_id,))
            row = cursor.fetchone()

            if row:
                customer = Customer.create_with_dict(row)
                return customer
            else:
                return None



    def get_customer_by_national_code(self, national_code):
        with self.creat_connection() as connection:
            cursor = connection.cursor(as_dict=True)
            cursor.execute("""select    Id  as  customer_id
                                           ,First_Name,Last_Name
                                           ,NationalCode,PhonNumber
                                           ,Email,BirthDate,Gender
                                   from Customer
                                   where NationalCode = %s""", (national_code,))
            row = cursor.fetchone()

            if row:
                customer = Customer.create_with_dict(row)
                return customer
            else:
                return None



    def create_customer(self, first_name, last_name, national_code, phon_number, email, birth_date, gender):
        with self.creat_connection() as connection :
            cursor = connection.cursor(as_dict=True)
            cursor.execute("""  insert Customer(First_Name,Last_Name,NationalCode,PhonNumber,Email,BirthDate,Gender)
                                values (%s,%s,%s,%s,%s,%s,%d)"""
                                ,(first_name,last_name,national_code,phon_number,email,birth_date,gender))
            connection.commit()
        return cursor.rowcount


    def update_customer(self,customer_id,firstname,lastname,national_code,phon_number,email,birth_date,gender):
        with self.creat_connection() as connection :
            cursor = connection.cursor(as_dict=True)
            cursor.execute("""  update Customer
                                set  First_Name = %s
                                ,	Last_Name = %s
                                ,   NationalCode = %s
                                ,	phonnumber = %s
                                ,	email = %s
                                ,	birthdate = %s
                                ,	gender = %d
                                 where id = %d""",(firstname,lastname,national_code,phon_number
                                                                                  ,email,birth_date,gender,customer_id))
            connection.commit()
        return cursor.rowcount

    def deactivated_customer(self, customer_id):
        with self.creat_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""update Account
                            set StatusId = %d 
                            where Customer_Id =%d """,(2,customer_id))
            connection.commit()
        return cursor.rowcount

    def blocked_customer(self, customer_id):
        with self.creat_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""update Account
                            set StatusId = %d 
                            where Customer_Id =%d """, (3, customer_id))
            connection.commit()
        return cursor.rowcount



