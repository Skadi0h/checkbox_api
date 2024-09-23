from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from piccolo_api.csrf.middleware import CSRFMiddleware

from checkbox_api.apps.common import app_lifespan

from checkbox_api.apps.public import app as public_app
from checkbox_api.apps.secured import app as secured_app

from checkbox_api.config import APP_CONFIG, RunModes

app = FastAPI(
    root_path='/api/v1',
    lifespan=app_lifespan
)

app.mount(path='/protected', app=secured_app)
app.mount(path='/public', app=public_app)


if APP_CONFIG.run_mode == RunModes.PRODUCTION:
    app.add_middleware(
        CSRFMiddleware
    )
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=APP_CONFIG.allowed_hosts
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=APP_CONFIG.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
