import datetime
import enum
import uuid

from sqlmodel import SQLModel, Field, Relationship


class PaymentTypes(enum.StrEnum):
    CASH = enum.auto()
    CASHLESS = enum.auto()


class ReceiptCommon(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(...)
    payment_type: PaymentTypes = Field(...)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)


class ReceiptDB(ReceiptCommon, table=True):
    __tablename__ = 'receipts'

    user_id: uuid.UUID = Field(foreign_key='users.id')
    proof_id: uuid.UUID = Field(foreign_key='proofs.id')

    user: "UserDB" = Relationship(  # type: ignore[name-defined]
        back_populates='receipts'
    )
    proof: "ProofDB" = Relationship(  # type: ignore[name-defined]
        back_populates='receipts'
    )
    products: list["ProductDB"] = Relationship(  # type: ignore[name-defined]
        back_populates='receipt'
    )
