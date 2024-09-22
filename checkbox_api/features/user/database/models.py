import uuid

from sqlmodel import (
    SQLModel,
    Field, Relationship
)

from checkbox_api.mixins.password import PasswordManagementMixin


class UserCommon(SQLModel, table=False):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    first_name: str = Field(max_length=64)
    last_name: str = Field(max_length=64)
    login: str = Field(max_length=64, unique=True, index=True)


class UserDB(
    UserCommon,
    PasswordManagementMixin,
    table=True
):
    __tablename__ = 'users'

    hashed_password: str = Field(...)
    receipts: list['ReceiptDB'] = Relationship(  # type: ignore[name-defined]
        back_populates='user'
    )

    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'
