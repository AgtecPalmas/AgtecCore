from decouple import config

APP_ID = "{{ cookiecutter.project_slug }}"

ELASTIC_APM = {
    "SERVICE_NAME": "{{ cookiecutter.project_slug }}",
    "SERVER_URL": config("ELASTIC_APM_SERVER_URL"),
    "DEBUG": config("DEBUG", default=False, cast=bool),
    "ENVIRONMENT": config("ENVIRONMENT", default="desenvolvimento"),
}