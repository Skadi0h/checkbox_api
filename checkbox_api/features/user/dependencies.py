from typing import Annotated

import fastapi


class UserContext:

    def __init__(self):
        ...


async def _user_context_dependency(

) -> UserContext:
    return UserContext()


UserContextDependency = Annotated[
    UserContext,
    fastapi.Depends(
        _user_context_dependency
    )
]
