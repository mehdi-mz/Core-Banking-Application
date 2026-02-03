from BusinessLogic.transaction_business_logic import TransactionBusinessLogic
from DataAccess.Repositories.SQLServer.sql_server_transaction_repository import SqlServerTransactionRepository
from DataAccess.Repositories.SQLServer.sql_server_customer_repository import SqlServerCustomerRepository
from BusinessLogic.account_business_logic import AccountBusinessLogic
from DataAccess.Repositories.SQLServer.sql_server_account_repository import SqlServerAccountRepository
from BusinessLogic.customer_business_logic import CustomerBusinessLogic

def get_transaction_business():
    transaction_repository = SqlServerTransactionRepository()
    account_repository = SqlServerAccountRepository()
    customer_repository = SqlServerCustomerRepository()

    business = TransactionBusinessLogic(transaction_repository,account_repository,customer_repository)
    return business


def account_business_logic():
    repository = SqlServerAccountRepository()

    business = AccountBusinessLogic(repository)
    return business


def customer_business_logic():
    customer_repository = SqlServerCustomerRepository()
    business = CustomerBusinessLogic(customer_repository)
    return business
