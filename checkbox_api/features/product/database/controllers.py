from checkbox_api.features.product.database.models import ProductDB
from checkbox_api.generics.controller import (
    ReadInstanceController,
    CreateInstanceController
)


class ProductController(
    ReadInstanceController[ProductDB],
    CreateInstanceController[ProductDB]
):
    __cls__ = ProductDB
