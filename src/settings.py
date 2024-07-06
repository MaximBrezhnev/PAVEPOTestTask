import os

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class ProjectSettings(BaseSettings):
    APP_TITLE: str
    API_URL_PREFIX: str
    APP_HOST: str
    APP_PORT: int

    PWD_SCHEMA: str
    PWD_DEPRECATED: str

    CELERY_BROKER_HOST: str
    CELERY_RESULT_BACKEND_HOST: str
    CELERY_BROKER_PORT: int
    CELERY_RESULT_BACKEND_PORT: int

    REDIRECT_URI: str
    VK_API_VERSION: str
    VK_API_URL: str

    @property
    def CELERY_BROKER_URL(self):
        return f"redis://{self.CELERY_BROKER_HOST}:{self.CELERY_BROKER_PORT}"

    @property
    def CELERY_RESULT_BACKEND_URL(self):
        return f"redis://{self.CELERY_RESULT_BACKEND_HOST}:{self.CELERY_RESULT_BACKEND_PORT}"

    model_config = SettingsConfigDict(
        env_file=os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            ".env"
        ),
        extra="ignore",
    )


project_settings = ProjectSettings()
