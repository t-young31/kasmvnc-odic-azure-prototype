import os
import jwt
from fastapi import FastAPI, Request, Response, status, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from base64 import b64encode

app = FastAPI()


class User(BaseModel):
    username: str


@app.get("/")
async def root(response: Response):
    response.status_code = status.HTTP_200_OK
    return {"message": "Hello World"}


@app.get("/me", response_model=User)
async def me(request: Request, response: Response):

    print(request.headers)

    try:
        username = request.headers['x-forwarded-preferred-username']
        response.status_code = status.HTTP_200_OK
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    return User(username=username)


@app.get("/vm")
async def vm(request: Request):


    token = request.headers["x-forwarded-access-token"]
    # TODO: verify JWT. see https://github.com/microsoft/AzureTRE/blob/8c82fd75ee9ad48c6fd7f257ca1ecc8055e57852/api_app/services/aad_authentication.py#L144
    payload = jwt.decode(token, algorithms=['RS256'], options={"verify_signature": False})
    print(payload)

    if "x-forwarded-preferred-username" not in request.headers:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
   
    return RedirectResponse(os.environ["KASM_URL"], status_code=status.HTTP_302_FOUND)
