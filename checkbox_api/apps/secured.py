import fastapi
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

from checkbox_api.features.receipt.api.router import router as receipt_router


app = FastAPI(
    description='Secured CheckBox API',
    dependencies=[
        fastapi.Depends(OAuth2PasswordBearer(tokenUrl='/api/v1/public/sign-in'))
    ]
)

app.include_router(
    router=receipt_router
)

__all__ = [
    'app'
]
