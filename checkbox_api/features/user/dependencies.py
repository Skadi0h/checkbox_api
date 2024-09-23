import logging
from typing import Annotated

import fastapi
from fastapi import HTTPException

from checkbox_api.auth.access_token import decode_access_token
from checkbox_api.dependencies.database import DBSession
from checkbox_api.dependencies.logger import LoggerDependency
from checkbox_api.features.user.database.controller import UserController
from checkbox_api.features.user.database.models import UserCommon, UserDB


async def _user_controller_dependency(
        *,
        session: DBSession,
        logger: Annotated[logging.Logger, fastapi.Depends(
            LoggerDependency(name='UserController Logger')
        )]
) -> UserController:
    return UserController(
        session=session,
        logger=logger
    )


UserControllerDependency = Annotated[
    UserController,
    fastapi.Depends(
        _user_controller_dependency
    )
]


async def get_current_user(
        *,
        request: fastapi.Request,
        user_controller: UserControllerDependency,
        logger: Annotated[logging.Logger, fastapi.Depends(
            LoggerDependency(name='get current user logger')
        )]
) -> UserCommon:

    try:
        user_data = decode_access_token(token=request.headers['Authorization'].split('Bearer ')[1])
        return UserCommon.model_validate(
            obj=await user_controller.read_one(
                filter_chain=(
                    UserDB.id == user_data['user_id'],
                )
            )
        )
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=401)


CurrentUserDependency = Annotated[
    UserCommon,
    fastapi.Depends(
        get_current_user
    )
]

__all__ = [
    'UserControllerDependency'
]
