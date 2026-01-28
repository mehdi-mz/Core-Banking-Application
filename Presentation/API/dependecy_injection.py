from BusinessLogic.transaction_business_logic import TransactionBusinessLogic
from DataAccess.Repositories.SQLServer.sql_server_transaction_repository import SqlServerTransactionRepository
from DataAccess.Repositories.SQLServer.sql_server_account_repository import SqlServerAccountRepository
from DataAccess.Repositories.SQLServer.sql_server_customer_repository import SqlServerCustomerRepository

def get_transaction_business():
    transaction_repository = SqlServerTransactionRepository()
    account_repository = SqlServerAccountRepository()
    customer_repository = SqlServerCustomerRepository()

    business = TransactionBusinessLogic(transaction_repository,account_repository,customer_repository)
    return business