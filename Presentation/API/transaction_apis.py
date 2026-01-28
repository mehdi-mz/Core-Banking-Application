from fastapi import APIRouter , Query ,Depends
from Presentation.API.dependecy_injection import get_transaction_business
from BusinessLogic.transaction_business_logic import TransactionBusinessLogic


router = APIRouter(prefix="/api/v1/transactions",tags=["Transaction"])


@router.get("/")
def get_transaction_api(account_number:int
                        ,page_number:int=Query(default=1,ge=1)
                        ,page_size:int=Query(default=15,le=20)
                        ,transaction_business:TransactionBusinessLogic = Depends(get_transaction_business) ):
    response = transaction_business.get_transaction_list(account_number,page_number,page_size)

    if response.success:
        return response.data