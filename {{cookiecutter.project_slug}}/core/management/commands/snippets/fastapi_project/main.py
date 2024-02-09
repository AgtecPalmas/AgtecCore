from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from core.config import settings
from core.routers import api_router

app = FastAPI(title=settings.app_name, openapi_url=f"{settings.api_str}/openapi.json")

# Set all CORS enabled origins
if settings.backend_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.backend_cors_origins],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

if settings.debug is False:
    import sentry_sdk
    from elasticapm.contrib.starlette import ElasticAPM

    from core.elastic import ELASTIC_APM

    sentry_sdk.init(
        dsn=settings.sentry_dsn, enable_tracing=True, environment=settings.environment
    )

    app.add_middleware(
        ElasticAPM,
        client=ELASTIC_APM,
    )
else:
    from core.middlewares.log import CustomLog

    app.add_middleware(
        CustomLog,
    )

app.include_router(api_router)
