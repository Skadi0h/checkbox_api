from checkbox_api.features.proof.database.models import ProofDB
from checkbox_api.generics.controller import (
    ReadInstanceController,
    CreateInstanceController
)


class ProofController(
    ReadInstanceController[ProofDB],
    CreateInstanceController[ProofDB]
):
    __cls__ = ProofDB
