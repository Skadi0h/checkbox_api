from checkbox_api.features.user.database.models import UserCommon


class UserCreate(UserCommon):
    password: str


class UserOutput(UserCommon):
    ...


class UserUpdate(UserCreate):
    ...
