from checkbox_api.features.receipt.database.models import ReceiptDB
from checkbox_api.generics.controller import (
    ReadInstanceController,
    CreateInstanceController
)


class ReceiptController(
    ReadInstanceController[ReceiptDB],
    CreateInstanceController[ReceiptDB]
):
    __cls__ = ReceiptDB
