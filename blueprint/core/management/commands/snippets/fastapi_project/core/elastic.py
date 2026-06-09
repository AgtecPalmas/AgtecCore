from elasticapm.contrib.starlette import make_apm_client

from core.config import settings

APP_ID = settings.app_name


ELASTIC_APM = make_apm_client(
    {
        "SERVICE_NAME": APP_ID,
        "SERVER_URL": settings.elastic_apm_server_url,
        "DEBUG": False,
        "ENVIRONMENT": settings.environment,
    }
)
