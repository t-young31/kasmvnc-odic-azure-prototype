import os
import jwt
from fastapi import FastAPI, Request, Response, status, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from base64 import b64encode

app = FastAPI()


class User(BaseModel):
    email: str


@app.get("/")
async def root(response: Response):
    response.status_code = status.HTTP_200_OK
    return {"message": "Hello World. Check out routes /me and /vm"}


@app.get("/me", response_model=User)
async def me(request: Request, response: Response):

    print("Headers: \n", {k: v for k, v in request.headers.items() if k != "cookie"})
    token = request.headers["x-access-token"]
    # TODO: verify JWT. see https://github.com/microsoft/AzureTRE/blob/8c82fd75ee9ad48c6fd7f257ca1ecc8055e57852/api_app/services/aad_authentication.py#L144
    payload = jwt.decode(token, algorithms=['RS256'], options={"verify_signature": False})
    print("JWT:\n", payload)

    try:
        email = request.headers['x-email']
        response.status_code = status.HTTP_200_OK
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    return User(email=email)


@app.get("/vm")
async def vm(request: Request):

    if "x-email" not in request.headers:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
   
    return RedirectResponse(os.environ["KASM_URL"], status_code=status.HTTP_302_FOUND)
