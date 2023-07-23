from fastapi import FastAPI
from router import auth

app = FastAPI()

app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
