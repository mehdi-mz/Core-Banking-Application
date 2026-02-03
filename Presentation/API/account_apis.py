from fastapi import APIRouter , Query , Depends ,HTTPException
from typing import Optional
from Presentation.API.dependecy_injection import account_business_logic
from Presentation.API.DTOs.create_account_dto import CreateAccountDTO
from Presentation.API.DTOs.message_response_dto import MessageResponseDTO
from Presentation.API.DTOs.update_account_dto import UpdateAccountDTO
from BusinessLogic.account_business_logic import AccountBusinessLogic
from Common.entities.Enums.account_status import AccountStatus
from Common.entities.Enums.account_types import AccountTypes

router_accounts = APIRouter(prefix="/api/v1/accounts",tags=["Account"])


@router_accounts.get("/")
def get_accounts_api(page_number:int=Query(default=1,ge=1)
                     ,page_size:int=Query(default=15,le=20)
                     ,search:Optional[str]=Query(default=None)
                     ,account_business:AccountBusinessLogic=Depends(account_business_logic)):

    try:
        response = account_business.get_account_list(page_number, page_size,search)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if  not response.success:
        raise HTTPException(status_code=400, detail=response.message)
    return [
        {
            "account_number": t.account_number,
            "customer_name": f"{t.customer.firstname} {t.customer.lastname}",
            "customer_national_code":t.customer.national_code,
            "account_status": t.account_status.name,
            "created_date": t.created_date,
            "account_type": t.account_type.name,
        }
        for t in response.data
    ]



@router_accounts.post("/",response_model=MessageResponseDTO)
def create_account_api(create_account: CreateAccountDTO
                       ,account_business:AccountBusinessLogic=Depends(account_business_logic)):

    try:
        account_status = AccountStatus(create_account.account_status_id)
    except ValueError:
        raise HTTPException(status_code=400,detail="Invalid Account Status Id.")

    try:
        account_type = AccountTypes(create_account.account_type_id)
    except ValueError:
        raise HTTPException(status_code=400,detail="Invalid Account Type Id.")

    try:
        response = account_business.create_account(create_account.national_code,account_status
                                                   ,account_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if  not response.success:
        raise HTTPException(status_code=400, detail=response.message)
    return {"message": "Account Created.✅"}



# @router_accounts.put("/",response_model=MessageResponseDTO)
# def update_account_api(account_number:int
#                        ,update_account:UpdateAccountDTO
#                        ,account_business:AccountBusinessLogic=Depends(account_business_logic)):
#     if update_account.account_status_id  is not None:
#         try:
#             account_status = AccountStatus(update_account.account_status_id)
#         except ValueError:
#             raise HTTPException(status_code=400,detail="Invalid Account Status Id.")
#
#     if update_account.account_type_id is not None:
#         try:
#             account_type = AccountTypes(update_account.account_type_id)
#         except ValueError:
#             raise HTTPException(status_code=400,detail="Invalid Account Status Id.")
#
#     try:
#         response = account_business.update_account(account_number,account_type, account_status)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#
#     if  not response.success:
#         raise HTTPException(status_code=400, detail=response.message)
#
#     return {"message": "Account Updated.✅"}
#
# @router_accounts.delete("/")
# def block_account_api():
#     pass