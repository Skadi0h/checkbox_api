import logging
from typing import Annotated

import fastapi

from checkbox_api.dependencies.database import DBSession
from checkbox_api.dependencies.logger import LoggerDependency
from checkbox_api.features.product.database.controllers import ProductController


async def _product_controller_dependency(
        *,
        session: DBSession,
        logger: Annotated[logging.Logger, fastapi.Depends(
            LoggerDependency(name='ProductController Logger')
        )]
) -> ProductController:
    return ProductController(
        session=session,
        logger=logger
    )


ProductControllerDependency = Annotated[
    ProductController,
    fastapi.Depends(
        _product_controller_dependency
    )
]
