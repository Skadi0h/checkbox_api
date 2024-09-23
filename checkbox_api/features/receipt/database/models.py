import datetime
import enum
import uuid

from sqlmodel import SQLModel, Field, Relationship

from checkbox_api.features.product.database.models import ProductDB
from checkbox_api.features.proof.database.models import ProofDB
from checkbox_api.features.user.database.models import UserDB


class PaymentTypes(enum.StrEnum):
    CASH = enum.auto()
    CASHLESS = enum.auto()


class ReceiptCommon(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    payment_type: PaymentTypes = Field(...)
    created_at: int = Field(default_factory=datetime.datetime.timestamp)


class ReceiptDB(ReceiptCommon, table=True):
    __tablename__ = 'receipts'
    user_id: uuid.UUID = Field(foreign_key='users.id')
    user: UserDB = Relationship(
        back_populates='receipts'
    )
    proof: ProofDB = Relationship(
        back_populates='receipt'
    )
    products: list[ProductDB] = Relationship(
        back_populates='receipt'
    )
