import logging
from typing import Annotated, Literal

import fastapi
import sqlalchemy.exc
from fastapi import FastAPI
from pydantic import BaseModel
from starlette import status

from checkbox_api.auth.password import PasswordHelper
from checkbox_api.dependencies.logger import LoggerDependency
from checkbox_api.features.user.api.validation import UserCreate
from checkbox_api.features.user.database.models import UserDB
from checkbox_api.features.user.dependencies import UserControllerDependency

from checkbox_api.auth.access_token import create_access_token

app = FastAPI(
    title='Public CheckBox API',
    description='Public CheckBox API'
)


class SignInModel(BaseModel):
    username: str
    password: str


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: Literal['Bearer']


@app.post('/sign-up', status_code=status.HTTP_201_CREATED, tags=['Registration'])
async def sign_up(
        *,
        user: Annotated[UserCreate, fastapi.Body()],
        user_controller: UserControllerDependency,
        logger: Annotated[
            logging.Logger,
            fastapi.Depends(
                LoggerDependency(
                    name='Sign In Logger'
                )
            )
        ]
) -> AccessTokenResponse:
    try:
        if await user_controller.exists(filter_chain=(UserDB.login == user.login,)):
            raise fastapi.HTTPException(status_code=401, detail='User exists')
        db_user = await user_controller.upsert_one(
            instance=UserDB(
                **user.model_dump(
                    exclude={'password'}
                ),
                hashed_password=PasswordHelper.create_hashed_password(
                    password=user.password
                )
            )
        )
    except sqlalchemy.exc.SQLAlchemyError as e:
        logger.exception(e)
        raise fastapi.HTTPException(status_code=401, detail='Authorization error')
    except fastapi.HTTPException as e:
        logger.exception(e)
        raise e
    except Exception as e:
        logger.exception(e)
        raise fastapi.HTTPException(status_code=500, detail='Unhandled exception')
    else:
        access_token = create_access_token(user_id=db_user.id)

    return AccessTokenResponse(
        access_token=access_token,
        token_type='Bearer'
    )


@app.post('/sign-in', tags=['Auth'])
async def sign_in(
        *,
        user_data: Annotated[SignInModel, fastapi.Form()],
        user_controller: UserControllerDependency,
        logger: Annotated[
            logging.Logger,
            fastapi.Depends(
                LoggerDependency(
                    name='Sign In Logger'
                )
            )
        ]
) -> AccessTokenResponse:
    try:
        user = await user_controller.read_one(filter_chain=(UserDB.login == user_data.username,))
        assert PasswordHelper.verify_password(
            password=user_data.password,
            hashed_password=user.hashed_password
        )
    except sqlalchemy.exc.NoResultFound as e:
        logger.exception(e)
        raise fastapi.HTTPException(status_code=401, detail='Authorization error')
    except Exception as e:
        logger.exception(e)
        raise fastapi.HTTPException(status_code=500, detail='Unhandled exception')
    else:
        access_token = create_access_token(user_id=user.id)

    return AccessTokenResponse(
        access_token=access_token,
        token_type='Bearer'
    )


__all__ = [
    'app'
]
