import logging
from typing import Annotated

import fastapi

from checkbox_api.dependencies.database import DBSession
from checkbox_api.dependencies.logger import LoggerDependency
from checkbox_api.features.product.dependencies import ProductControllerDependency
from checkbox_api.features.receipt.database.controllers import ReceiptController
from checkbox_api.features.receipt.handlers import ReceiptHandler
from checkbox_api.features.user.dependencies import CurrentUserDependency


async def _receipt_controller_dependency(
        *,
        session: DBSession,
        logger: Annotated[logging.Logger, fastapi.Depends(
            LoggerDependency(name='ReceiptController Logger')
        )]
) -> ReceiptController:
    return ReceiptController(
        session=session,
        logger=logger
    )


ReceiptControllerDependency = Annotated[
    ReceiptController,
    fastapi.Depends(
        _receipt_controller_dependency
    )
]


async def _receipt_handler_dependency(
        *,
        user: CurrentUserDependency,
        receipt_controller: ReceiptControllerDependency,
        product_controller: ProductControllerDependency
) -> ReceiptHandler:
    return ReceiptHandler(
        user=user,
        receipt_controller=receipt_controller,
        product_controller=product_controller
    )


ReceiptHandlerDependency = Annotated[
    ReceiptHandler,
    fastapi.Depends(
        _receipt_handler_dependency
    )
]

__all__ = [
    'ReceiptControllerDependency',
    'ReceiptHandlerDependency',
]
