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
    from core.elastic import ELASTIC_APM

    app.add_middleware(
        ElasticAPM,
        client=ELASTIC_APM,
    )

app.include_router(api_router)
