from fastapi import FastAPI
from router import auth, create_item

app = FastAPI()

app.include_router(auth.router)
app.include_router(create_item.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
