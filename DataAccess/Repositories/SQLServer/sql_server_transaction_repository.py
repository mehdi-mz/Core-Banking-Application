import pymssql
from Common.Repositories.itransaction_repository import ITransactionRepository
from Common.entities.transaction import Transaction

class SqlServerTransactionRepository(ITransactionRepository):

    def creat_connection(self):
        connection=pymssql.connect(host=".",
        database="Bank Management Application")
        return connection



    def get_transactions(self, account_number: int, page_number=1, page_size=15):
        skip_rows= (page_number-1)*page_size
        transaction_list=[]
        with self.creat_connection() as connection:
            cursor = connection.cursor(as_dict=True)
            cursor.execute("""
            select Id, 
            Account_Number,
            Old_Balance,
            Amount,
            TransactionType,
            UserName,
            isnull(card,0)   as  card,
            transactiontime  as Transaction_Time
            from [transactions]
            where Account_Number = %d
            order by transactiontime desc 
            offset %d rows 
            fetch next %d rows only
            """,(account_number,skip_rows,page_size))
            data = cursor.fetchall()
            for row in data:
                transaction = Transaction.create_with_dict(row)
                transaction_list.append(transaction)
        return transaction_list




    def get_all_transactions(self, account_number: int):
        transaction_list=[]
        with self.creat_connection() as connection:
            cursor = connection.cursor(as_dict=True)
            cursor.execute("""
            select Id, 
            Account_Number,
            Old_Balance,
            Amount,
            TransactionType,
            UserName,
            isnull(card,0)   as  card,
            transactiontime   as Transaction_Time
            from [transactions]
            where Account_Number = %d
            order by transactiontime desc 
            """,(account_number,))
            data = cursor.fetchall()
            for row in data:
                transaction = Transaction.create_with_dict(row)
                transaction_list.append(transaction)
        return transaction_list


    def sum_balance(self,account_number):
        with self.creat_connection() as connection:
            cursor = connection.cursor(as_dict=True)
            cursor.execute("""
                            select  isnull(sum(iif(transactiontype=1,amount,iif(transactiontype=4
                            ,amount,-amount))),0) as total_balance
                            from transactions
                            where Account_Number = %d
            """,(account_number,))
            data = cursor.fetchone()
            balance = data.get("total_balance")
            return balance




    def insert_transaction(self,new_transaction : Transaction):
        with self.creat_connection() as connection:
            cursor = connection.cursor(as_dict=True)
            cursor.execute("""
            insert transactions(Account_Number,Old_Balance,Amount,TransactionType,UserName,TransactionTime)
            values(%d,%s,%d,%d,%s,%s) """,(new_transaction.account_number
                                                  ,new_transaction.old_balance
                                                  ,new_transaction.amount
                                                  ,new_transaction.transaction_type.value
                                                  ,new_transaction.user_name
                                                  ,new_transaction.transaction_time))
            connection.commit()

    def get_daily_transactions(self,account_number):
        daily_transaction_list=[]
        with self.creat_connection() as connection:
            cursor = connection.cursor(as_dict=True)
            cursor.execute("""
                            select  id , 
                                    Account_Number,
                                    Old_Balance,
                                    Amount,
                                    TransactionType,
                                    UserName,
                                    TransactionTime
                            from transactions
                            where Account_Number = %d
                            and TransactionType = 2
                            and convert(date,TransactionTime) = CONVERT(date , GETDATE())
                                        """,account_number)
            data  = cursor.fetchall()
            for row in data:
                transaction = Transaction.create_with_dict(row)
                daily_transaction_list.append(transaction)
        return daily_transaction_list



    def card_to_card(self, new_transaction,old_balance_card):
        with self.creat_connection() as connection:
            cursor = connection.cursor(as_dict=True)
            cursor.execute("""
                   insert transactions(Account_Number,Old_Balance,Amount,TransactionType,UserName,card,TransactionTime)
                   values(%d,%s,%d,%d,%s,%d,%s) """, (new_transaction.account_number
                                                          , new_transaction.old_balance
                                                          , new_transaction.amount
                                                          ,3
                                                          , new_transaction.user_name
                                                          ,new_transaction.card
                                                          , new_transaction.transaction_time))

            cursor.execute("""
                  insert transactions(Account_Number,Old_Balance,Amount,TransactionType,UserName,card,TransactionTime)
                  values(%d,%s,%d,%d,%s,%d,%s) """, (new_transaction.card
                                                 ,old_balance_card
                                                 , new_transaction.amount
                                                 , 4
                                                 , new_transaction.user_name
                                                 , new_transaction.account_number
                                                 ,new_transaction.transaction_time))
            connection.commit()



