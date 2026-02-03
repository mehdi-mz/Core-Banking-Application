from fastapi import APIRouter , Query ,Depends ,HTTPException
from Presentation.API.dependecy_injection import get_transaction_business
from BusinessLogic.transaction_business_logic import TransactionBusinessLogic
from Presentation.API.DTOs.create_transaction_dto import CreateTransactionDTO
from Presentation.API.DTOs.message_response_dto import MessageResponseDTO
from Common.entities.Enums.transaction_types import TransactionTypes


router_transactions = APIRouter(prefix="/api/v1/transactions",tags=["Transaction"])


@router_transactions.get("/")
def get_transaction_api(account_number:int =Query(ge=1000)
                        ,page_number:int=Query(default=1,ge=1)
                        ,page_size:int=Query(default=15,le=20)
                        ,transaction_business:TransactionBusinessLogic = Depends(get_transaction_business) ):
    try:
        response = transaction_business.get_transaction_list(account_number,page_number,page_size)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if  not response.success:
        raise HTTPException(status_code=400, detail=response.message)
    return [
        {
            "id": t.id,
            "account_number": t.account_number,
            "old_balance": t.old_balance,
            "amount": t.amount,
            "transaction_type": TransactionTypes(t.transaction_type).name,
            "username": t.user_name,
            "card": t.card,
            "transaction_time": t.transaction_time,
        }
        for t in response.data
    ]




@router_transactions.post("/",response_model=MessageResponseDTO)
def create_transaction_api( create_transaction : CreateTransactionDTO,
                            transaction_business:TransactionBusinessLogic = Depends(get_transaction_business)):

    username = "Customer"
    try:
        transaction_type = TransactionTypes(create_transaction.transaction_type_id)
    except ValueError:
        raise HTTPException(status_code=400,detail="Invalid Transaction Type Id.")

    card_number = create_transaction.card
    if not card_number:
        card_number = None

    try:
        response = transaction_business.create_transaction(create_transaction.amount,transaction_type
                                                           ,create_transaction.account_number,username,card_number)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if  not response.success:
        raise HTTPException(status_code=400, detail=response.message)

    return {"message": "Transaction Created.✅"}
