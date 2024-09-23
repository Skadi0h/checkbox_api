import uuid

from checkbox_api.features.product.database.controllers import ProductController
from checkbox_api.features.product.database.models import ProductDB
from checkbox_api.features.product.validation import ProductOutput
from checkbox_api.features.receipt.api.validation import ReceiptCreate, ReceiptOutput, ReceiptFilters
from checkbox_api.features.receipt.database.controllers import ReceiptController
from checkbox_api.features.receipt.database.models import ReceiptDB
from checkbox_api.features.user.database.models import UserCommon


class ReceiptHandler:

    def __init__(
            self,
            *,
            user: UserCommon,
            receipt_controller: ReceiptController,
            product_controller: ProductController,
    ) -> None:
        self._receipt_controller = receipt_controller
        self._product_controller = product_controller
        self._user = user

    async def create_receipt(
            self,
            *,
            receipt: ReceiptCreate
    ) -> ReceiptOutput:
        created_receipt = await self._receipt_controller.upsert_one(
            instance=ReceiptDB(
                user_id=self._user.id,
                **receipt.model_dump(exclude={'products'})
            )
        )
        created_products = await self._product_controller.insert_many(
            instances=[
                ProductDB(
                    receipt_id=created_receipt.id,
                    **product.model_dump()
                )
                for product in receipt.products
            ]
        )

        return ReceiptOutput(
            id=created_receipt.id,
            user_id=created_receipt.user_id,
            payment_type=created_receipt.payment_type,
            products=[
                ProductOutput.model_validate(
                    obj=product
                )
                for product in created_products
            ],
            created_at=created_receipt.created_at

        )

    async def get_receipt_by_id(self, *, receipt_id: uuid.UUID) -> ReceiptOutput:
        ...

    async def get_receipts_by_filters(
            self,
            *,
            receipt_filters: ReceiptFilters
    ) -> list[ReceiptOutput]:
        ...
