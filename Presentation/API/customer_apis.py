from fastapi import APIRouter , Query ,Depends ,HTTPException
from Presentation.API.dependecy_injection import customer_business_logic
from Presentation.API.DTOs.create_customer_dto import CreateCustomerDTO
from Presentation.API.DTOs.message_response_dto import MessageResponseDTO
from typing import Optional
from BusinessLogic.customer_business_logic import CustomerBusinessLogic
from Common.entities.Enums.gender import Gender
router_customer = APIRouter(prefix="/api/v1/customers",tags=["Customer"])


@router_customer.get("/")
def get_customer_api( page_number:int=Query(default=1,ge=1)
                      , page_size:int=Query(default=15,ge=15,le=20)
                      , search:Optional[str]=Query(default=None)
                      , customer_business:CustomerBusinessLogic =Depends(customer_business_logic)):
    try:
        response = customer_business.get_customers(page_number, page_size,search)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not response.success:
        raise HTTPException(status_code=400, detail=response.message)
    return [
        {
            "id": t.customer_id,
            "customer_name": f"{t.firstname} {t.lastname}",
            "national_code": t.national_code,
            "phon_number": t.phon_number,
            "email": t.email,
            "birth_date": t.birth_date,
            "gender": t.gender.name,

        }
        for t in response.data
    ]

@router_customer.post("/",response_model=MessageResponseDTO)
def create_customer_api(create_customer : CreateCustomerDTO
                        ,customer_business:CustomerBusinessLogic =Depends(customer_business_logic)):
    try:
        gender = Gender(create_customer.gender_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Gender Id.")

    try:
        response = customer_business.create_customer(create_customer.firstname,create_customer.lastname,create_customer.national_code
                                                     ,create_customer.phon_number,create_customer.email,create_customer.birth_date,gender)
    except Exception as e :
        raise HTTPException(status_code=500, detail=str(e))

    if not response.success:
        raise HTTPException(status_code=400,detail=response.message)

    return {"message": "Customer Created.✅"}

#
# @router_customer.put("/")
# def update_customer_api():
#     pass

#
# @router_customer.get("/")
# def block_customer_api():
#     pass
#
#
# @router_customer.get("/")
# def deactive_customer_api():
#     pass


