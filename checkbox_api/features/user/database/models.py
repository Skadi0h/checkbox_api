import uuid

from sqlmodel import (
    SQLModel,
    Field, Relationship
)

class UserCommon(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    first_name: str = Field(max_length=64)
    last_name: str = Field(max_length=64)
    login: str = Field(max_length=64, unique=True, index=True)


class UserDB(
    UserCommon,
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
