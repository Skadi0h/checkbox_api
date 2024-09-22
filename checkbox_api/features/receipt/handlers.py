import uuid

from checkbox_api.features.product.database.controllers import ProductController
from checkbox_api.features.receipt.api.validation import ReceiptCreate, ReceiptOutput, ReceiptFilters
from checkbox_api.features.receipt.database.controllers import ReceiptController
from checkbox_api.features.user.dependencies import UserContext


class ReceiptHandler:

    def __init__(
            self,
            *,
            user_context: UserContext,
            receipt_controller: ReceiptController,
            product_controller: ProductController,
    ) -> None:
        self._receipt_controller = receipt_controller
        self._product_controller = product_controller
        self._user_context = user_context

    async def create_receipt(
            self,
            *,
            receipt: ReceiptCreate
    ) -> ReceiptOutput:
        ...

    async def get_receipt_by_id(self, *, receipt_id: uuid.UUID) -> ReceiptOutput:
        ...

    async def get_receipts_by_filters(
            self,
            *,
            receipt_filters: ReceiptFilters
    ) -> list[ReceiptOutput]:
        ...
