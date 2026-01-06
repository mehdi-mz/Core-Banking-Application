from Common.entities.account import Account
from Common.entities.customer import Customer
from Common.Repositories.iaccount_repository import IAccountRepository
import pymssql


class SqlServerAccountRepository(IAccountRepository):

    def creat_connection(self):
        connection=pymssql.connect(host=".",database="Bank Management Application")
        return connection

    def get_account(self, page_number=1, page_size=15,term=None):
        account_list=[]
        skip_rows=(page_number-1)*page_size
        with self.creat_connection() as connection:
            cursor=connection.cursor(as_dict=True)
            if term:
                query = """select    Customer.Id  as   customer_id
                                    , Customer.First_Name
                                   ,Customer.Last_Name,Customer.NationalCode
                                   ,Customer.PhonNumber,Customer.Email
                                   ,Customer.BirthDate,Customer.Gender
                                   ,Account.Account_Number
                                   ,Account.StatusId
                                   ,Account.Created_Date
                                   ,Account.AccountTypeId
                           from Customer
                           inner join 
                                 Account
                           on	 Customer.Id = Account.Customer_Id
                           where First_Name    like %s
                           or    Last_Name     like %s
                           or    NationalCode  like %s
                           order by Created_Date  desc 
                           offset %d rows 
                           fetch next %d  rows only
                           """
                value = f'%{term}%'
                cursor.execute(query,(value,value,value,skip_rows,page_size))
                data = cursor.fetchall()
                for row in data:
                    customer = Customer.create_with_dict(row)
                    account = Account.create_with_dict(row,customer)
                    account_list.append(account)

            else:
                cursor.execute("""
                                        select Account.Account_Number
                                        ,		Account.StatusId
                                        ,		Account.Created_Date
                                        ,		Account.AccountTypeId
                                        ,		Customer.Id    as  customer_id
                                        ,		Customer.First_Name
                                        ,		Customer.Last_Name
                                        ,		Customer.NationalCode
                                        ,		Customer.PhonNumber
                                        ,		Customer.Email
                                        ,		Customer.BirthDate
                                        ,		Customer.Gender
                                        from  Account
                                        inner join 
                                              Customer
                                        on    Customer.Id = Account.Customer_Id
                                        order by Created_Date  desc 
                                        offset %d rows 
                                        fetch next %d  rows only
                                        """, (skip_rows, page_size))
                data = cursor.fetchall()
                for row in data:
                    costomer = Customer.create_with_dict(row)
                    account = Account.create_with_dict(row, costomer)
                    account_list.append(account)

        return account_list

    def get_account_by_id(self, account_number:int):
        with self.creat_connection() as connection:
            cursor = connection.cursor(as_dict=True)
            cursor.execute("""
                                select Account.Account_Number
                                ,		Account.StatusId
                                ,		Account.Created_Date
                                ,		Account.AccountTypeId
                                ,		Customer.Id    as  customer_id
                                ,		Customer.First_Name
                                ,		Customer.Last_Name
                                ,		Customer.NationalCode
                                ,		Customer.PhonNumber
                                ,		Customer.Email
                                ,		Customer.BirthDate
                                ,		Customer.Gender
                                from  Account
                                inner join 
                                      Customer
                                on    Customer.Id = Account.Customer_Id
                                where Account.Account_Number = %d
                                order by Created_Date  desc 
                                  """,account_number)
            row = cursor.fetchone()

            if row :
                costomer = Customer.create_with_dict(row)
                account = Account.create_with_dict(row,costomer)
        return account

    def create_account(self, national_code, status_id,type_id):
        with self.creat_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(""" DECLARE @NationalCode NVARCHAR(10) = %s
                                        DECLARE @CustomerId INT
                                        
                                        SELECT @CustomerId = Id
                                        FROM Customer
                                        WHERE NationalCode = @NationalCode
                                        
                                        INSERT Account (Customer_Id, StatusId, AccountTypeId)
                                        VALUES (@CustomerId, %d, %d);""",(national_code,status_id,type_id))
            connection.commit()
        return cursor.rowcount


    def update_account(self, account_number, account_type, account_status):
        with self.creat_connection() as connection:
            cursor = connection.cursor(as_dict=True)
            cursor.execute("""  update Account
                                set AccountTypeId = %d
                                ,   StatusId      =  %d
                                where Account_Number = %d """,(account_type,account_status,account_number))
            connection.commit()
            return cursor.rowcount


    def customer_accounts(self, customer_id):
        account_list= []
        with self.creat_connection() as connection :
            cursor = connection.cursor(as_dict=True)
            cursor.execute("""select Account.Account_Number
                                ,		Account.StatusId
                                ,		Account.Created_Date
                                ,		Account.AccountTypeId
                                ,		Customer.Id    as  customer_id
                                ,		Customer.First_Name
                                ,		Customer.Last_Name
                                ,		Customer.NationalCode
                                ,		Customer.PhonNumber
                                ,		Customer.Email
                                ,		Customer.BirthDate
                                ,		Customer.Gender
                                from  Account
                                inner join 
                                      Customer
                                on    Customer.Id = Account.Customer_Id
                                where Account.Customer_Id = %d
                                order by Created_Date  desc """,(customer_id,))
            data = cursor.fetchall()
            for row in data:
                costomer = Customer.create_with_dict(row)
                account = Account.create_with_dict(row,costomer)
                account_list.append(account)
        return account_list











