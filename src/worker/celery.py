from celery import Celery

from src.settings import project_settings
from src.worker.utils import send_messages

celery: Celery = Celery("worker")
celery.conf.broker_url = project_settings.CELERY_BROKER_URL
celery.conf.result_backend = project_settings.CELERY_RESULT_BACKEND_URL


VK_API_URL = "https://api.vk.com/method/messages.send"
VK_API_VERSION = "5.131"


@celery.task
def send_messages_task(message: str):
    send_messages(message)


