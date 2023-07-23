from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import Response
from router import auth, create_item
from conf import FASTAPI_ALLOWED_HOSTS

app = FastAPI()


# 自定义中间件，用于限制hosts
async def check_host_middleware(request: Request, call_next):
    allowed_hosts = FASTAPI_ALLOWED_HOSTS.split(";")  # 允许的hosts列表
    if request.headers["host"] not in allowed_hosts and allowed_hosts != []:
        print(request.headers["host"])
        return Response(status_code=403)

    response = await call_next(request)
    return response


# 添加中间件到应用程序
app.middleware("http")(check_host_middleware)

app.include_router(auth.router)
app.include_router(create_item.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
