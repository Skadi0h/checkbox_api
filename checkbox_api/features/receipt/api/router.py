import uuid
from typing import Annotated

import fastapi
from fastapi_utils.cbv import cbv

from checkbox_api.features.receipt.api.validation import (
    ReceiptCreate,
    ReceiptOutput,
    ReceiptFilters
)
from checkbox_api.features.receipt.dependencies import ReceiptHandlerDependency

router = fastapi.APIRouter(
    prefix='/receipts',
    tags=['Receipts']
)


@cbv(router)
class ReceiptAPI:

    @router.post('/')
    async def create_receipt(
            self,
            *,
            payload: Annotated[ReceiptCreate, fastapi.Body()],
            receipt_handler: ReceiptHandlerDependency
    ) -> ReceiptOutput:
        return await receipt_handler.create_receipt(
            receipt=payload
        )

    @router.get('/')
    async def get_receipts(
            self,
            *,
            receipt_filters: Annotated[ReceiptFilters, fastapi.Query()],
            receipt_handler: ReceiptHandlerDependency
    ) -> list[ReceiptOutput]:
        return await receipt_handler.get_receipts_by_filters(
            receipt_filters=receipt_filters
        )

    @router.get('/{receipt_id:uuid}')
    async def get_receipt_by_id(
            self,
            *,
            receipt_id: Annotated[uuid.UUID, fastapi.Path()],
            receipt_handler: ReceiptHandlerDependency
    ) -> ReceiptOutput:
        return await receipt_handler.get_receipt_by_id(receipt_id=receipt_id)
