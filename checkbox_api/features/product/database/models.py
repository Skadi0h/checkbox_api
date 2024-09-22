import decimal
import uuid

from sqlmodel import SQLModel, Field, Relationship


class ProductCommon(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    receipt_id: uuid.UUID | None = None
    name: str = Field(
        max_length=128,
        index=True
    )
    description: str = Field(
        max_length=512
    )
    count: int = Field(gt=1)
    price_unit: decimal.Decimal = Field(gt=0)
    weight_unit: decimal.Decimal = Field(gt=0)
    total_price: decimal.Decimal = Field(gt=0)
    total_weight: decimal.Decimal | None = Field(nullable=True)


class ProductDB(ProductCommon, table=True):
    __tablename__ = 'products'
    receipt_id: uuid.UUID = Field(foreign_key='receipts.id')
    receipt: 'ReceiptDB' = Relationship(  # type: ignore[name-defined]
        back_populates='products'
    )
