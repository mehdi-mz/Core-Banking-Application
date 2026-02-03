from fastapi import  FastAPI
from Presentation.API.transaction_apis import router_transactions
from Presentation.API.account_apis import router_accounts
from Presentation.API.customer_apis import router_customer

app=FastAPI(title="Core Banking API")

app.include_router(router_transactions)
app.include_router(router_customer)
app.include_router(router_accounts)