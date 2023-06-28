import os
from fastapi import FastAPI, Request, Response, status, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel


app = FastAPI()


class User(BaseModel):
    username: str


@app.get("/")
async def root(response: Response):
    response.status_code = status.HTTP_200_OK
    return {"message": "Hello World"}


@app.get("/me", response_model=User)
async def me(request: Request, response: Response):

    try:
        username = request.headers['x-forwarded-preferred-username']
        response.status_code = status.HTTP_200_OK
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    return User(username=username)


@app.get("/vm")
async def vm(request: Request):

    if "x-forwarded-preferred-username" not in request.headers:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    return RedirectResponse(os.environ["KASM_URL"], status_code=status.HTTP_302_FOUND)
