import uuid

from sqlmodel import SQLModel, Field, Relationship


class ProofCommon(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    receipt_id: uuid.UUID | None = None


class ProofDB(ProofCommon, table=True):
    __tablename__ = 'proofs'
    receipt_id: uuid.UUID = Field(foreign_key='receipts.id')
    receipt: 'ReceiptDB' = Relationship(  # type: ignore[name-defined]
        sa_relationship_kwargs={'uselist': False},
        back_populates='proof'
    )
