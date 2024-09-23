from checkbox_api.features.user.database.models import UserDB
from checkbox_api.generics.controller import ReadInstanceController, CreateInstanceController


class UserController(
    ReadInstanceController[UserDB],
    CreateInstanceController[UserDB]
):
    __cls__ = UserDB