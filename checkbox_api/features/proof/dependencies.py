import logging
from typing import Annotated

import fastapi

from checkbox_api.dependencies.database import DBSession
from checkbox_api.dependencies.logger import LoggerDependency
from checkbox_api.features.proof.database.controllers import ProofController


async def _proof_controller_dependency(
        *,
        session: DBSession,
        logger: Annotated[logging.Logger, fastapi.Depends(
            LoggerDependency(name='Proof Controller Logger')
        )]
) -> ProofController:
    return ProofController(
        session=session,
        logger=logger
    )


ProofControllerDependency = Annotated[
    ProofController,
    fastapi.Depends(
        _proof_controller_dependency
    )
]
