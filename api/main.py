from fastapi import FastAPI, Request, Response, status, HTTPException
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
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid")

    return User(username=username)
