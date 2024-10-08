import decimal
import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from checkbox_api.features.product.database.models import ProductCommon
from checkbox_api.features.product.validation import ProductCreate
from checkbox_api.features.receipt.database.models import ReceiptCommon, PaymentTypes


class ReceiptCreate(ReceiptCommon):
    products: list[ProductCreate]


class ReceiptOutput(ReceiptCommon):
    products: list[ProductCommon]


class ReceiptFilters(BaseModel):
    date_from: datetime | None = Field(...)
    date_to: datetime | None = Field(...)
    min_amount: decimal.Decimal | None = Field(...)
    max_amount: decimal.Decimal | None = Field(...)
    payment_type: PaymentTypes = Field(...)
    user_ids: list[uuid.UUID] = Field(...)
