import requests
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import database_settings
from src.sender.models import Account, Contact
from src.settings import project_settings


def get_access_token(
        code: str,
        client_id: int,
        client_secret: str,
        redirect_uri: str
) -> str:
    url = f"https://oauth.vk.com/access_token?client_id={client_id}&client_secret={client_secret}&redirect_uri={redirect_uri}&code={code}"
    response = requests.get(url)
    data = response.json()
    return data.get('access_token')


def send_vk_message(vk_id: str, message: str, access_token: str) -> dict:
    params = {
        "user_id": vk_id,
        "message": message,
        "access_token": access_token,
        "v": project_settings.VK_API_VERSION
    }
    response = requests.post(project_settings.VK_API_URL, params=params)
    return response.json()


def get_accounts(db: Session):
    result = db.execute(select(Account))
    return result.scalars().all()


def get_contacts(db: Session):
    result = db.execute(select(Contact))
    return result.scalars().all()


def send_messages(message: str) -> None:
    db_session = database_settings.session()

    with db_session.begin():
        accounts = get_accounts(db_session)
        contacts = get_contacts(db_session)
        contact_iter = iter(contacts)

        for account in accounts:
            try:
                contact = next(contact_iter)
                send_vk_message(contact.vk_id, message, get_access_token(
                        code=account.code,
                        client_id=account.client_id,
                        client_secret=account.client_secret,
                        redirect_uri=project_settings.REDIRECT_URI
                ))
            except StopIteration:
                break
