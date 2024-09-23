from typing import Annotated

import fastapi
from fastapi_utils.cbv import cbv

from checkbox_api.features.user.api.validation import UserCreate, UserOutput

router = fastapi.APIRouter(
    prefix='/users'
)


@cbv(router)
class UserManagement:
    @router.post("/sign-in")
    def sign_in(
        self,
        *,
        user: Annotated[UserCreate, fastapi.Body()]
    ) -> UserOutput:
        ...
