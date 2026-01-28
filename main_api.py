from fastapi import  FastAPI
from Presentation.API.transaction_apis import router

app=FastAPI(title="Core Banking API")

app.include_router(router)


@app.get("/say_hello")
def say_hello():
    return {"message":"Hello"}


